from ledger import Ledger


def main():
    a = [1, 2, 3]
    b = [4, 5, 6]
    ledger1 = Ledger()
    block1 = ledger1.speculate(None, "1", a)
    block2 = ledger1.speculate(block1, "2", b)
    commit1 = ledger1.commit(block2)
    commit2 = ledger1.pending_state(block2)
    data = ledger1.commited_block(block2)
    print(data)
    data = ledger1.commited_block(block1)
    print(data)


if __name__ == "__main__":
    main()
