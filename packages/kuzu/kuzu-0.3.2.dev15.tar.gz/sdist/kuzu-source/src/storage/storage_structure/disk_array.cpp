#include "storage/storage_structure/disk_array.h"

#include "common/cast.h"
#include "common/string_format.h"
#include "common/utils.h"

using namespace kuzu::common;
using namespace kuzu::transaction;

namespace kuzu {
namespace storage {

DiskArrayHeader::DiskArrayHeader(uint64_t elementSize)
    : alignedElementSizeLog2{(uint64_t)ceil(log2(elementSize))},
      numElementsPerPageLog2{BufferPoolConstants::PAGE_4KB_SIZE_LOG2 - alignedElementSizeLog2},
      elementPageOffsetMask{BitmaskUtils::all1sMaskForLeastSignificantBits(numElementsPerPageLog2)},
      firstPIPPageIdx{DBFileUtils::NULL_PAGE_IDX}, numElements{0}, numAPs{0} {}

void DiskArrayHeader::saveToDisk(FileHandle& fileHandle, uint64_t headerPageIdx) {
    fileHandle.getFileInfo()->writeFile(reinterpret_cast<uint8_t*>(this), sizeof(DiskArrayHeader),
        headerPageIdx * fileHandle.getPageSize());
}

void DiskArrayHeader::readFromFile(FileHandle& fileHandle, uint64_t headerPageIdx) {
    fileHandle.getFileInfo()->readFromFile(reinterpret_cast<uint8_t*>(this),
        sizeof(DiskArrayHeader), headerPageIdx * fileHandle.getPageSize());
}

PIPWrapper::PIPWrapper(FileHandle& fileHandle, page_idx_t pipPageIdx) : pipPageIdx(pipPageIdx) {
    fileHandle.readPage(reinterpret_cast<uint8_t*>(&pipContents), pipPageIdx);
}

BaseDiskArrayInternal::BaseDiskArrayInternal(
    FileHandle& fileHandle, page_idx_t headerPageIdx, uint64_t elementSize)
    : header{elementSize}, fileHandle{fileHandle}, headerPageIdx{headerPageIdx},
      hasTransactionalUpdates{false}, bufferManager{nullptr}, wal{nullptr} {}

BaseDiskArrayInternal::BaseDiskArrayInternal(FileHandle& fileHandle, DBFileID dbFileID,
    page_idx_t headerPageIdx, BufferManager* bufferManager, WAL* wal,
    transaction::Transaction* transaction)
    : fileHandle{fileHandle}, dbFileID{dbFileID}, headerPageIdx{headerPageIdx},
      hasTransactionalUpdates{false}, bufferManager{bufferManager}, wal{wal} {
    auto [fileHandleToPin, pageIdxToPin] = DBFileUtils::getFileHandleAndPhysicalPageIdxToPin(
        ku_dynamic_cast<FileHandle&, BMFileHandle&>(fileHandle), headerPageIdx, *wal,
        transaction->getType());
    bufferManager->optimisticRead(*fileHandleToPin, pageIdxToPin,
        [&](uint8_t* frame) -> void { memcpy(&header, frame, sizeof(DiskArrayHeader)); });
    if (this->header.firstPIPPageIdx != DBFileUtils::NULL_PAGE_IDX) {
        pips.emplace_back(fileHandle, header.firstPIPPageIdx);
        while (pips[pips.size() - 1].pipContents.nextPipPageIdx != DBFileUtils::NULL_PAGE_IDX) {
            pips.emplace_back(fileHandle, pips[pips.size() - 1].pipContents.nextPipPageIdx);
        }
    }
}

uint64_t BaseDiskArrayInternal::getNumElements(TransactionType trxType) {
    std::shared_lock sLck{diskArraySharedMtx};
    return getNumElementsNoLock(trxType);
}

uint64_t BaseDiskArrayInternal::getNumElementsNoLock(TransactionType trxType) {
    return readUInt64HeaderFieldNoLock(trxType,
        [](DiskArrayHeader* diskArrayHeader) -> uint64_t { return diskArrayHeader->numElements; });
}

bool BaseDiskArrayInternal::checkOutOfBoundAccess(TransactionType trxType, uint64_t idx) {
    auto currentNumElements = getNumElementsNoLock(trxType);
    if (idx >= currentNumElements) {
        // LCOV_EXCL_START
        throw RuntimeException(stringFormat(
            "idx: {} of the DiskArray to be accessed is >= numElements in DiskArray{}.", idx,
            currentNumElements));
        // LCOV_EXCL_STOP
    }
    return true;
}

void BaseDiskArrayInternal::get(uint64_t idx, TransactionType trxType, std::span<uint8_t> val) {
    std::shared_lock sLck{diskArraySharedMtx};
    KU_ASSERT(checkOutOfBoundAccess(trxType, idx));
    auto apCursor = getAPIdxAndOffsetInAP(idx);
    page_idx_t apPageIdx = getAPPageIdxNoLock(apCursor.pageIdx, trxType);
    auto& bmFileHandle = (BMFileHandle&)fileHandle;
    if (trxType == TransactionType::READ_ONLY || !hasTransactionalUpdates ||
        !bmFileHandle.hasWALPageVersionNoWALPageIdxLock(apPageIdx)) {
        bufferManager->optimisticRead(bmFileHandle, apPageIdx, [&](const uint8_t* frame) -> void {
            memcpy(val.data(), frame + apCursor.elemPosInPage, val.size());
        });
    } else {
        ((BMFileHandle&)fileHandle).acquireWALPageIdxLock(apPageIdx);
        DBFileUtils::readWALVersionOfPage(bmFileHandle, apPageIdx, *bufferManager, *wal,
            [&val, &apCursor](const uint8_t* frame) -> void {
                memcpy(val.data(), frame + apCursor.elemPosInPage, val.size());
            });
    }
}

void BaseDiskArrayInternal::update(uint64_t idx, std::span<uint8_t> val) {
    std::unique_lock xLck{diskArraySharedMtx};
    hasTransactionalUpdates = true;
    KU_ASSERT(checkOutOfBoundAccess(TransactionType::WRITE, idx));
    auto apCursor = getAPIdxAndOffsetInAP(idx);
    // TODO: We are currently supporting only DiskArrays that can grow in size and not
    // those that can shrink in size. That is why we can use
    // getAPPageIdxNoLock(apIdx, Transaction::WRITE) directly to compute the physical page Idx
    // because any apIdx is guaranteed to be either in an existing PIP or a new PIP we added, which
    // getAPPageIdxNoLock will correctly locate: this function simply searches an existing PIP if
    // apIdx < numAPs stored in "previous" PIP; otherwise one of the newly inserted PIPs stored in
    // pipPageIdxsOfInsertedPIPs. If within a single transaction we could grow or shrink, then
    // getAPPageIdxNoLock logic needs to change to give the same guarantee (e.g., an apIdx = 0, may
    // no longer to be guaranteed to be in pips[0].)
    page_idx_t apPageIdx = getAPPageIdxNoLock(apCursor.pageIdx, TransactionType::WRITE);
    DBFileUtils::updatePage((BMFileHandle&)fileHandle, dbFileID, apPageIdx,
        false /* not inserting a new page */, *bufferManager, *wal,
        [&apCursor, &val](uint8_t* frame) -> void {
            memcpy(frame + apCursor.elemPosInPage, val.data(), val.size());
        });
}

uint64_t BaseDiskArrayInternal::pushBack(std::span<uint8_t> val) {
    std::unique_lock xLck{diskArraySharedMtx};
    hasTransactionalUpdates = true;
    return pushBackNoLock(val);
}

uint64_t BaseDiskArrayInternal::resize(uint64_t newNumElements, std::span<uint8_t> defaultVal) {
    std::unique_lock xLck{diskArraySharedMtx};
    hasTransactionalUpdates = true;
    auto currentNumElements = getNumElementsNoLock(TransactionType::WRITE);
    while (currentNumElements < newNumElements) {
        pushBackNoLock(defaultVal);
        currentNumElements++;
    }
    return currentNumElements;
}

uint64_t BaseDiskArrayInternal::pushBackNoLock(std::span<uint8_t> val) {
    uint64_t elementIdx;
    DBFileUtils::updatePage((BMFileHandle&)(fileHandle), dbFileID, headerPageIdx,
        false /* not inserting a new page */, *bufferManager, *wal,
        [this, &val, &elementIdx](uint8_t* frame) -> void {
            auto updatedDiskArrayHeader = ((DiskArrayHeader*)frame);
            elementIdx = updatedDiskArrayHeader->numElements;
            auto apCursor = getAPIdxAndOffsetInAP(elementIdx);
            auto [apPageIdx, isNewlyAdded] = getAPPageIdxAndAddAPToPIPIfNecessaryForWriteTrxNoLock(
                (DiskArrayHeader*)frame, apCursor.pageIdx);
            // Now do the push back.
            DBFileUtils::updatePage((BMFileHandle&)(fileHandle), dbFileID, apPageIdx, isNewlyAdded,
                *bufferManager, *wal, [&apCursor, &val](uint8_t* frame) -> void {
                    memcpy(frame + apCursor.elemPosInPage, val.data(), val.size());
                });
            updatedDiskArrayHeader->numElements++;
        });
    return elementIdx;
}

uint64_t BaseDiskArrayInternal::getNumAPsNoLock(TransactionType trxType) {
    return readUInt64HeaderFieldNoLock(trxType,
        [](DiskArrayHeader* diskArrayHeader) -> uint64_t { return diskArrayHeader->numAPs; });
}

void BaseDiskArrayInternal::setNextPIPPageIDxOfPIPNoLock(DiskArrayHeader* updatedDiskArrayHeader,
    uint64_t pipIdxOfPreviousPIP, page_idx_t nextPIPPageIdx) {
    // This happens if the first pip is being inserted, in which case we need to change the header.
    if (pipIdxOfPreviousPIP == UINT64_MAX) {
        updatedDiskArrayHeader->firstPIPPageIdx = nextPIPPageIdx;
    } else {
        page_idx_t pipPageIdxOfPreviousPIP = getUpdatedPageIdxOfPipNoLock(pipIdxOfPreviousPIP);
        /*
         * Note that we can safely pass insertingNewPage argument here. There are two cases;
         * 1) if pipPageIdxOfPreviousPIP is a new PIP: in that case the previous caller
         * would have already created the WAL page for it, so this function is not creating
         * pipPageIdxOfPreviousPIP. 2) if pipPageIdxOfPreviousPIP is an existing PIP, in which
         * case again this function is not creating pipPageIdxOfPreviousPIP.
         */
        DBFileUtils::updatePage((BMFileHandle&)fileHandle, dbFileID, pipPageIdxOfPreviousPIP,
            false /* not inserting a new page */, *bufferManager, *wal,
            [&nextPIPPageIdx](
                const uint8_t* frame) -> void { ((PIP*)frame)->nextPipPageIdx = nextPIPPageIdx; });
        // The above updatePage operation changes the "previousPIP" identified by
        // pipIdxOfPreviousPIP, so we put it to updatedPIPIdxs if it was a pip that already existed
        // before this transaction started. If pipIdxOfPreviousPIP >= pips.size() then it must
        // already be in pipUpdates.pipPageIdxsOfInsertedPIPs, so we do not need to insert it to
        // pipUpdates.pipPageIdxsOfInsertedPIPs (and hence there is no else to the below if).
        if (pipIdxOfPreviousPIP < pips.size()) {
            pipUpdates.updatedPipIdxs.insert(pipIdxOfPreviousPIP);
        }
    }
}

page_idx_t BaseDiskArrayInternal::getAPPageIdxNoLock(page_idx_t apIdx, TransactionType trxType) {
    auto pipIdxAndOffset = StorageUtils::getQuotientRemainder(apIdx, NUM_PAGE_IDXS_PER_PIP);
    uint64_t pipIdx = pipIdxAndOffset.first;
    uint64_t offsetInPIP = pipIdxAndOffset.second;
    if ((trxType == TransactionType::READ_ONLY) || !hasPIPUpdatesNoLock(pipIdx)) {
        return pips[pipIdx].pipContents.pageIdxs[offsetInPIP];
    } else {
        page_idx_t retVal;
        page_idx_t pageIdxOfUpdatedPip = getUpdatedPageIdxOfPipNoLock(pipIdx);
        ((BMFileHandle&)fileHandle).acquireWALPageIdxLock(pageIdxOfUpdatedPip);
        DBFileUtils::readWALVersionOfPage((BMFileHandle&)fileHandle, pageIdxOfUpdatedPip,
            *bufferManager, *wal, [&retVal, &offsetInPIP](const uint8_t* frame) -> void {
                retVal = ((PIP*)frame)->pageIdxs[offsetInPIP];
            });
        return retVal;
    }
}

page_idx_t BaseDiskArrayInternal::getUpdatedPageIdxOfPipNoLock(uint64_t pipIdx) {
    if (pipIdx < pips.size()) {
        return pips[pipIdx].pipPageIdx;
    }
    return pipUpdates.pipPageIdxsOfInsertedPIPs[pipIdx - pips.size()];
}

void BaseDiskArrayInternal::clearWALPageVersionAndRemovePageFromFrameIfNecessary(
    page_idx_t pageIdx) {
    ((BMFileHandle&)this->fileHandle).clearWALPageIdxIfNecessary(pageIdx);
    bufferManager->removePageFromFrameIfNecessary((BMFileHandle&)this->fileHandle, pageIdx);
}

void BaseDiskArrayInternal::checkpointOrRollbackInMemoryIfNecessaryNoLock(bool isCheckpoint) {
    if (!hasTransactionalUpdates) {
        return;
    }
    // Note: We update the header regardless (even if it has not changed). We can optimize this
    // by adding logic that keep track of whether the header has been updated.
    if (isCheckpoint) {
        header.readFromFile(this->fileHandle, headerPageIdx);
    }
    clearWALPageVersionAndRemovePageFromFrameIfNecessary(headerPageIdx);
    for (uint64_t pipIdxOfUpdatedPIP : pipUpdates.updatedPipIdxs) {
        // Note: This should not cause a memory leak because PIPWrapper is a struct. So we
        // should overwrite the previous PIPWrapper's memory.
        if (isCheckpoint) {
            pips[pipIdxOfUpdatedPIP] = PIPWrapper(fileHandle, pips[pipIdxOfUpdatedPIP].pipPageIdx);
        }
        clearWALPageVersionAndRemovePageFromFrameIfNecessary(pips[pipIdxOfUpdatedPIP].pipPageIdx);
    }

    for (page_idx_t pipPageIdxOfNewPIP : pipUpdates.pipPageIdxsOfInsertedPIPs) {
        if (isCheckpoint) {
            pips.emplace_back(fileHandle, pipPageIdxOfNewPIP);
        }
        clearWALPageVersionAndRemovePageFromFrameIfNecessary(pipPageIdxOfNewPIP);
        if (!isCheckpoint) {
            // These are newly inserted pages, so we can truncate the file handle.
            ((BMFileHandle&)this->fileHandle)
                .removePageIdxAndTruncateIfNecessary(pipPageIdxOfNewPIP);
        }
    }
    // Note that we already updated the header to its correct state above.
    pipUpdates.clear();
    hasTransactionalUpdates = false;
}

bool BaseDiskArrayInternal::hasPIPUpdatesNoLock(uint64_t pipIdx) {
    // This is a request to a pipIdx > pips.size(). Since pips.size() is the original number of pips
    // we started with before the write transaction is updated, we return true, i.e., this PIP is
    // an "updated" PIP and should be read from the WAL version.
    if (pipIdx >= pips.size()) {
        return true;
    }
    return pipUpdates.updatedPipIdxs.contains(pipIdx);
}

uint64_t BaseDiskArrayInternal::readUInt64HeaderFieldNoLock(
    TransactionType trxType, std::function<uint64_t(DiskArrayHeader*)> readOp) {
    // TODO(Guodong): Fix the casting here, which can be incorrect for HashIndexBuilder.
    auto bmFileHandle = reinterpret_cast<BMFileHandle*>(&fileHandle);
    if ((trxType == TransactionType::READ_ONLY) ||
        !bmFileHandle->hasWALPageVersionNoWALPageIdxLock(headerPageIdx)) {
        return readOp(&this->header);
    } else {
        uint64_t retVal;
        ((BMFileHandle&)fileHandle).acquireWALPageIdxLock(headerPageIdx);
        DBFileUtils::readWALVersionOfPage((BMFileHandle&)fileHandle, headerPageIdx, *bufferManager,
            *wal, [&retVal, &readOp](uint8_t* frame) -> void {
                retVal = readOp((DiskArrayHeader*)frame);
            });
        return retVal;
    }
}

std::pair<page_idx_t, bool>
BaseDiskArrayInternal::getAPPageIdxAndAddAPToPIPIfNecessaryForWriteTrxNoLock(
    DiskArrayHeader* updatedDiskArrayHeader, page_idx_t apIdx) {
    if (apIdx < updatedDiskArrayHeader->numAPs) {
        // If the apIdx of the array page is < updatedDiskArrayHeader->numAPs, we do not have to
        // add a new array page, so directly return the pageIdx of the apIdx.
        return std::make_pair(getAPPageIdxNoLock(apIdx, TransactionType::WRITE),
            false /* is not inserting a new ap page */);
    } else {
        // apIdx even if it's being inserted should never be > updatedDiskArrayHeader->numAPs.
        KU_ASSERT(apIdx == updatedDiskArrayHeader->numAPs);
        // We need to add a new AP. This may further cause a new pip to be inserted, which is
        // handled by the if/else-if/else branch below.
        page_idx_t newAPPageIdx = fileHandle.addNewPage();
        // We need to create a new array page and then add its apPageIdx (newAPPageIdx variable) to
        // an appropriate PIP.
        auto pipIdxAndOffsetOfNewAP =
            StorageUtils::getQuotientRemainder(apIdx, NUM_PAGE_IDXS_PER_PIP);
        uint64_t pipIdx = pipIdxAndOffsetOfNewAP.first;
        uint64_t offsetOfNewAPInPIP = pipIdxAndOffsetOfNewAP.second;
        updatedDiskArrayHeader->numAPs++;
        page_idx_t pipPageIdx = DBFileUtils::NULL_PAGE_IDX;
        bool isInsertingANewPIPPage = false;
        if (pipIdx < pips.size()) {
            // We do not need to insert a new pip and we need to add newAPPageIdx to a PIP that
            // existed before this transaction started.
            pipUpdates.updatedPipIdxs.insert(pipIdx);
            pipPageIdx = pips[pipIdx].pipPageIdx;
        } else if ((pipIdx - pips.size()) < pipUpdates.pipPageIdxsOfInsertedPIPs.size()) {
            // We do not need to insert a new PIP and we need to add newAPPageIdx to a new PIP that
            // already got created after this transaction started.
            pipPageIdx = pipUpdates.pipPageIdxsOfInsertedPIPs[pipIdx - pips.size()];
        } else {
            // We need to create a new PIP and make the previous PIP (or the header) point to it.
            isInsertingANewPIPPage = true;
            pipPageIdx = fileHandle.addNewPage();
            pipUpdates.pipPageIdxsOfInsertedPIPs.push_back(pipPageIdx);
            uint64_t pipIdxOfPreviousPIP = pipIdx - 1;
            setNextPIPPageIDxOfPIPNoLock(updatedDiskArrayHeader, pipIdxOfPreviousPIP, pipPageIdx);
        }
        // Finally we update the PIP page (possibly newly created) and add newAPPageIdx into it.
        DBFileUtils::updatePage((BMFileHandle&)fileHandle, dbFileID, pipPageIdx,
            isInsertingANewPIPPage, *bufferManager, *wal,
            [&isInsertingANewPIPPage, &newAPPageIdx, &offsetOfNewAPInPIP](
                const uint8_t* frame) -> void {
                if (isInsertingANewPIPPage) {
                    ((PIP*)frame)->nextPipPageIdx = DBFileUtils::NULL_PAGE_IDX;
                }
                ((PIP*)frame)->pageIdxs[offsetOfNewAPInPIP] = newAPPageIdx;
            });
        return std::make_pair(newAPPageIdx, true /* inserting a new ap page */);
    }
}

BaseInMemDiskArray::BaseInMemDiskArray(FileHandle& fileHandle, DBFileID dbFileID,
    page_idx_t headerPageIdx, BufferManager* bufferManager, WAL* wal,
    transaction::Transaction* transaction)
    : BaseDiskArrayInternal(fileHandle, dbFileID, headerPageIdx, bufferManager, wal, transaction) {
    for (page_idx_t apIdx = 0; apIdx < this->header.numAPs; ++apIdx) {
        addInMemoryArrayPageAndReadFromFile(this->getAPPageIdxNoLock(apIdx));
    }
}

BaseInMemDiskArray::BaseInMemDiskArray(
    FileHandle& fileHandle, page_idx_t headerPageIdx, uint64_t elementSize)
    : BaseDiskArrayInternal(fileHandle, headerPageIdx, elementSize) {}

// [] operator to be used when building an InMemDiskArrayBuilder without transactional updates.
// This changes the contents directly in memory and not on disk (nor on the wal)
uint8_t* BaseInMemDiskArray::operator[](uint64_t idx) {
    auto apCursor = BaseDiskArrayInternal::getAPIdxAndOffsetInAP(idx);
    KU_ASSERT(apCursor.pageIdx < this->header.numAPs);
    return inMemArrayPages[apCursor.pageIdx].get() + apCursor.elemPosInPage;
}

void BaseInMemDiskArray::addInMemoryArrayPageAndReadFromFile(page_idx_t apPageIdx) {
    uint64_t apIdx = this->addInMemoryArrayPage(false /* setToZero */);
    readArrayPageFromFile(apIdx, apPageIdx);
}

void BaseInMemDiskArray::readArrayPageFromFile(uint64_t apIdx, page_idx_t apPageIdx) {
    this->fileHandle.readPage(
        reinterpret_cast<uint8_t*>(this->inMemArrayPages[apIdx].get()), apPageIdx);
}

InMemDiskArrayInternal::InMemDiskArrayInternal(FileHandle& fileHandle, DBFileID dbFileID,
    page_idx_t headerPageIdx, BufferManager* bufferManager, WAL* wal,
    transaction::Transaction* transaction)
    : BaseInMemDiskArray(fileHandle, dbFileID, headerPageIdx, bufferManager, wal, transaction) {}

void InMemDiskArrayInternal::checkpointOrRollbackInMemoryIfNecessaryNoLock(bool isCheckpoint) {
    if (!this->hasTransactionalUpdates) {
        return;
    }
    uint64_t numOldAPs = this->getNumAPsNoLock(TransactionType::READ_ONLY);
    for (uint64_t apIdx = 0; apIdx < numOldAPs; ++apIdx) {
        uint64_t apPageIdx = this->getAPPageIdxNoLock(apIdx, TransactionType::READ_ONLY);
        if (ku_dynamic_cast<FileHandle&, BMFileHandle&>(this->fileHandle)
                .hasWALPageVersionNoWALPageIdxLock(apPageIdx)) {
            // Note we can directly read the new image from disk because the WALReplayer checkpoints
            // the disk image of the page before calling
            // InMemDiskArray::checkpointInMemoryIfNecessary.
            if (isCheckpoint) {
                this->readArrayPageFromFile(apIdx, apPageIdx);
            }
            this->clearWALPageVersionAndRemovePageFromFrameIfNecessary(apPageIdx);
        }
    }
    uint64_t newNumAPs = this->getNumAPsNoLock(TransactionType::WRITE);
    // When rolling back, unlike removing new PIPs in
    // BaseDiskArray::checkpointOrRollbackInMemoryIfNecessaryNoLock when rolling back, we cannot
    // directly truncate each page. Instead we need to keep track of the minimum apPageIdx we
    // saw that we want to truncate to first. Then we call
    // BaseDiskArray::checkpointOrRollbackInMemoryIfNecessaryNoLock, which can do its own
    // truncation due to newly added PIPs. Then finally we truncate. The reason is this: suppose
    // we added a new apIdx=1 with pageIdx 20 in the fileHandle, which suppose caused a new PIP
    // to be inserted with pageIdx 21, and we further added one more new apIdx=2 with
    // pageIdx 22. Now this function will loop through the newly added apIdxs, so apIdx=1 and 2
    // in that order. If we directly truncate to the pageIdx of apIdx=1, which is 20, then we
    // will remove 21 and 22. But then we will loop through apIdx=2 and we need to convert it to
    // its pageIdx to clear its updated WAL version. But that requires reading the newly added
    // PIP's WAL version, which had pageIdx 22 but no longer exists. That would lead to a seg
    // fault somewhere. So we do not truncate these in order not to accidentally remove newly
    // added PIPs, which we would need if we kept calling removePageIdxAndTruncateIfNecessary
    // for each newly added array pages.
    page_idx_t minNewAPPageIdxToTruncateTo = INVALID_PAGE_IDX;
    for (uint64_t apIdx = this->header.numAPs; apIdx < newNumAPs; apIdx++) {
        page_idx_t apPageIdx = this->getAPPageIdxNoLock(apIdx, TransactionType::WRITE);
        if (isCheckpoint) {
            this->addInMemoryArrayPageAndReadFromFile(apPageIdx);
        }
        this->clearWALPageVersionAndRemovePageFromFrameIfNecessary(apPageIdx);
        if (!isCheckpoint) {
            minNewAPPageIdxToTruncateTo = std::min(minNewAPPageIdxToTruncateTo, apPageIdx);
        }
    }

    // TODO(Semih): Currently we do not support truncating DiskArrays. When we support that, we
    // need to implement the logic to truncate InMemArrayPages as well.
    // Note that the base class call sets hasTransactionalUpdates to false.
    if (isCheckpoint) {
        BaseDiskArrayInternal::checkpointOrRollbackInMemoryIfNecessaryNoLock(
            true /* is checkpoint */);
    } else {
        BaseDiskArrayInternal::checkpointOrRollbackInMemoryIfNecessaryNoLock(
            false /* is rollback */);
        ((BMFileHandle&)this->fileHandle)
            .removePageIdxAndTruncateIfNecessary(minNewAPPageIdxToTruncateTo);
    }
}

InMemDiskArrayBuilderInternal::InMemDiskArrayBuilderInternal(FileHandle& fileHandle,
    page_idx_t headerPageIdx, uint64_t numElements, size_t elementSize, bool setToZero)
    : BaseInMemDiskArray(fileHandle, headerPageIdx, elementSize) {
    setNumElementsAndAllocateDiskAPsForBuilding(numElements);
    for (uint64_t i = 0; i < this->header.numAPs; ++i) {
        this->addInMemoryArrayPage(setToZero);
    }
}

void InMemDiskArrayBuilderInternal::resize(uint64_t newNumElements, bool setToZero) {
    uint64_t oldNumAPs = this->header.numAPs;
    setNumElementsAndAllocateDiskAPsForBuilding(newNumElements);
    uint64_t newNumAPs = this->header.numAPs;
    for (auto i = oldNumAPs; i < newNumAPs; ++i) {
        this->addInMemoryArrayPage(setToZero);
    }
}

void InMemDiskArrayBuilderInternal::saveToDisk() {
    // save the header and pips.
    this->header.saveToDisk(this->fileHandle, this->headerPageIdx);
    for (auto i = 0u; i < this->pips.size(); ++i) {
        this->fileHandle.writePage(
            reinterpret_cast<uint8_t*>(&this->pips[i].pipContents), this->pips[i].pipPageIdx);
    }
    // Save array pages
    for (page_idx_t apIdx = 0; apIdx < this->header.numAPs; ++apIdx) {
        this->fileHandle.writePage(reinterpret_cast<uint8_t*>(this->inMemArrayPages[apIdx].get()),
            this->getAPPageIdxNoLock(apIdx));
    }
}

void InMemDiskArrayBuilderInternal::addNewArrayPageForBuilding() {
    uint64_t arrayPageIdx = this->fileHandle.addNewPage();
    // The idx of the next array page will be exactly header.numArrayPages. That is why we first
    // find the pipIdx and offset in the PIP of the array page before incrementing
    // header.numArrayPages by 1.
    auto pipIdxAndOffset =
        StorageUtils::getQuotientRemainder(this->header.numAPs, NUM_PAGE_IDXS_PER_PIP);
    this->header.numAPs++;
    uint64_t pipIdx = pipIdxAndOffset.first;
    if (pipIdx == this->pips.size()) {
        uint64_t pipPageIdx = this->fileHandle.addNewPage();
        this->pips.emplace_back(pipPageIdx);
        if (pipIdx == 0) {
            this->header.firstPIPPageIdx = pipPageIdx;
        } else {
            this->pips[pipIdx - 1].pipContents.nextPipPageIdx = pipPageIdx;
        }
    }
    this->pips[pipIdx].pipContents.pageIdxs[pipIdxAndOffset.second] = arrayPageIdx;
}

void InMemDiskArrayBuilderInternal::setNumElementsAndAllocateDiskAPsForBuilding(
    uint64_t newNumElements) {
    uint64_t oldNumArrayPages = this->header.numAPs;
    uint64_t newNumArrayPages = getNumArrayPagesNeededForElements(newNumElements);
    for (auto i = oldNumArrayPages; i < newNumArrayPages; ++i) {
        addNewArrayPageForBuilding();
    }
    this->header.numElements = newNumElements;
    this->header.numAPs = newNumArrayPages;
}

} // namespace storage
} // namespace kuzu
