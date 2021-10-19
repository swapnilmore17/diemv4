from ledger import Ledger
from blocktree import VoteInfo, LedgerCommitInfo, VoteMsg, BlockTree
from datastructs import TimeoutInfo


class Safety:
    def __init__(self, block_tree_module, ledger_module, highest_vote_round):

        self.block_tree_module = block_tree_module
        self.ledger_module = ledger_module
        # self.__private_key = private_key # Own private key
        # self.__public_keys = public_keys # Public keys of all validators
        self.__highest_vote_round = highest_vote_round  # initially 0
        self.__highest_qc_round = None  # trying 0

    def __increase_highest_vote_round(self, round):
        # commit not to vote in rounds lower than round
        self.__highest_vote_round = max(round, self.__highest_vote_round)

    def __update_highest_qc_round(self, qc_round):
        self.__highest_qc_round = max(qc_round, self.__highest_qc_round)

    def __consecutive(self, block_round, round):
        return round + 1 == block_round

    def __safe_to_extend(self, block_round, qc_round, tc):
        return self.__consecutive(
            block_round,
            tc.round) and qc_round >= max(
            tc.tmo_high_qc_rounds)

    def __safe_to_vote(self, block_round, qc_round, tc):
        if block_round <= max(self.highest_vote_round, qc_round):
            # 1. must vote in monotonically increasing rounds // 2. must extend
            # a smaller round
            return False
            # Extending qc from previous round or safe to extend due to tc
        return self.__consecutive(
            block_round, qc_round) or self.__safe_to_extend(
            block_round, qc_round, tc)

    """
    Function safe to vote(block round, qc round, tc)
        if block round ≤ max{highest vote round, qc round} then
        // 1. must vote in monotonically increasing rounds // 2. must extend a smaller round
        return false
        // Extending qc from previous round or safe to extend due to tc
        return consecutive(block round, qc round) ∨ safe to extend(block round, qc round, tc)

    """

    def __safe_to_timeout(self, round, qc_round, tc):
        if qc_round < self.highest_qc_round or round <= max(
                self.highest_vote_round - 1, qc_round):
            # respect highest qc round and don’t timeout in a past round
            return False
        # qc or tc must allow entering the round to timeout
        return self.__consecutive(
            round, qc_round) or self.__consecutive(
            round, tc.round)

    """
    Function safe to timeout(round, qc round, tc)
        if qc round < highest qc round ∨ round ≤ max{highest vote round − 1, qc round} then
        // respect highest qc round and don’t timeout in a past round
        return false
        // qc or tc must allow entering the round to timeout
        return consecutive(round, qc round) ∨ consecutive(round, tc.round)

    """

    def __commit_state_id_candidate(self, block_round, qc):
        # find the committed id in case a qc is formed in the vote round if
        # consecutive(block round, qc.vote info.round) then
        if self.__consecutive(block_round, qc.vote_info.round):
            return self.ledger_module.pending_state(qc.id)
        else:
            return None

    """
    Function commit state id candidate(block round, qc)
        // find the committed id in case a qc is formed in the vote round
        if consecutive(block round, qc.vote info.round) then
        return Ledger.pending state(qc.id)
        Else
        return ⊥

    """

    def __valid_signatures(self):
        return True

    def make_vote(self, b, last_tc):
        qc_round = b.qc.vote_info.round
        if self.__valid_signatures() and self.__safe_to_vote(b.round, qc_round, last_tc):
            self.__update_highest_qc_round(qc_round)  # Protect qc round
            # Don’t vote again in this (or lower) round
            self.__increase_highest_vote_round(b.round)
            # VoteInfo carries the potential QC info with ids and rounds of the
            # parent QC
            exec_state_id = self.ledger_module.pending_state(b.id)
            vote_info = VoteInfo(
                b.id,
                b.round,
                b.qc.vote_info.id,
                qc_round,
                exec_state_id)
            ledger_commit_info = LedgerCommitInfo(
                self.__commit_state_id_candidate(
                    b.round, b.qc), hash(vote_info))
            return VoteMsg(
                vote_info,
                ledger_commit_info,
                self.block_tree_module.high_commit_qc)
        return None

        """
        Function make vote(b, last tc)
            qc round ← b.qc.vote info.round
            if valid signatures(b, last tc) ∧ safe to vote(b.round, qc round, last tc) then
            update highest qc round(qc round) // Protect qc round
            increase highest vote round(b.round) // Don’t vote again in this (or lower) round
            // VoteInfo carries the potential QC info with ids and rounds of the parent QC
            vote info ←VoteInfo⟨
                (id, round) ← (b.id, b.round),
                (parent id, parent round) ← (b.qc.vote info.id, qc round)
                exec state id ← Ledger.pending state(b.id) ⟩
            ledger commit info ←LedgerCommitInfo ⟨
                commit state id ← commit state id candidate(b.round, b.qc),
                vote info hash ← hash(vote info) ⟩
            return VoteMsg⟨vote info, ledger commit info, Block-Tree.high commit qc⟩
            return ⊥

        """

    def make_timeout(self, round, high_qc, last_tc):
        qc_round = high_qc.vote_info.round
        if self.__valid_signatures() and self.__safe_to_timeout(round, qc_round, last_tc):
            self.__increase_highest_vote_round(round)  # Stop voting for round
            return TimeoutInfo(round, high_qc)
        return None

    """
    Function make timeout(round, high qc, last tc)
        qc round ← high qc.vote info.round;
        if valid signatures(high qc, last tc) ∧ safe to timeout(round, qc round, last tc) then
        increase highest vote round(round) // Stop voting for round
        return TimeoutInfo⟨round, high qc⟩
        return ⊥

    """
