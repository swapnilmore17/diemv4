from pacemaker import Pacemaker
from blocktree import BlockTree
from treeutility import TreeUtility
from ledger import Ledger
from LeaderElection import LeaderElection
from mempool import Mempool
from datastructs import ProposalMsg
from safety import Safety


class Main:

    # wait for next event and call start_event_processing()

    def __init__(self, validator_list, validator_index, f_nodes):
        self.validator_index = validator_index
        self.f_nodes = f_nodes
        self.validator_list = validator_list
        self.ledger = Ledger()
        self.block_tree = BlockTree(self.ledger)

        self.safety = Safety(
            self.block_tree,
            self.ledger,
            0)  # remaining values
        self.pacemaker = Pacemaker(0, None, {}, self.safety, self.block_tree)
        self.mempool = Mempool()
        self.leader_election = LeaderElection(
            self.validator_list, 10, 0, self.ledger, self.pacemaker)  # remaining values

        print('Main initialized')
    # def start_event_processing(self,message,current_round, leader,f):

    def process_certificate_qc(self, qc):
        print('inside process qc')
        self.block_tree.process_qc(qc)
        print('processed qc')
        self.leader_election.update_leaders(qc)
        self.pacemaker.advance_round_qc(qc.vote_info.round)

        """
        Procedure process certificate qc(qc)
            Block-Tree.process qc(qc)
            LeaderElection.update leaders(qc)
            Pacemaker.advance round(qc.vote info.round)
        """

    def process_proposal_message(self, p, current_round):

        if p.block.id=='1':
            block_id=self.ledger.speculate(None,"1","str")
            
        print('main')
        self.process_certificate_qc(p.block.qc)
        print('main2')
        self.process_certificate_qc(p.high_commit)
        self.pacemaker.advance_round_tc(p.last_round_tc)
        round = self.pacemaker.current_round
        
        leader_index = self.leader_election.get_leader(current_round)
        leader = self.validator_list[leader_index]
        if p.block.round != round or p.sender != leader or p.author != leader:
            print('proposal message')
            return None
        self.block_tree.execute_and_insert(p)
        vote_msg = self.safety.make_vote(p.block, p.last_round_tc)
        if vote_msg:
            next_leader_index = self.leader_election.get_leader(
                current_round + 1)
            #next_leader = self.validator_list[next_leader_index]
            print('proposal message')
            return (vote_msg, next_leader_index)
        print('proposal message')
        return None

        """
        Procedure process proposal msg(P)
            process certificate qc(P.block.qc)
            process certificate qc(P.high commit qc)
            Pacemaker.advance round tc(P.last round tc)
            round ← Pacemaker.current round
            leader ← LeaderElection.get leader(current round)
            if P.block.round ̸= round ∨ P.sender ̸= leader ∨ P.block.author ̸= leader then
            Return
            Block-Tree.execute and insert(P) // Adds a new speculative state to the Ledger
            vote msg ← Safety.make vote(P.block, P.last round tc)
            if vote msg ̸= ⊥ then
            send vote msg to LeaderElection.get leader(current round + 1)

            Procedure process timeout msg(M)
            process certificate qc(M.tmo info.high qc)
            process certificate qc(M.high commit qc)
            Pacemaker.advance round tc(M.last round tc)
            tc ← Pacemaker.process remote timeout(M)
            if tc ̸= ⊥ then
            Pacemaker.advance round(tc)
            process new round event(tc)

        """

    def process_timeout_message(self, m, f):
        # print('main')
        self.process_certificate_qc(m.tmo_info.high_qc)
        self.process_certificate_qc(m.high_commit_qc)
        self.pacemaker.advance_round_tc(m.last_round_tc)
        tc = self.pacemaker.process_remote_timeout(m, f)
        if tc:
            self.pacemaker.advance_round(tc)
            msg = self.process_new_round_event(tc)
            return msg
        return None

    def process_vote_message(self, m):
        # print('main')
        qc = self.block_tree.process_vote(
            m, self.f_nodes, self.validator_list[self.validator_index])
        if qc:
            self.process_certificate_qc(qc)
            msg = self.process_new_round_event(None)
            return msg
        return None

        """
        Procedure process vote msg(M)
            qc ← Block-Tree.process vote(M)
            if qc ̸= ⊥ then
            process certificate qc(qc)
            process new round event(⊥)

        """

    def process_new_round_event(self, last_tc):
        # print('main')
        if self.leader_election.get_leader(
                self.pacemaker.current_round) == self.validator_index:
            b = self.block_tree.generate_block(
                self.mempool.get_transactions(),
                self.pacemaker.current_round)
            # add author of block
            msg = ProposalMsg(b, last_tc, self.block_tree.high_commit_qc)
            return msg
        return None

        """
        Procedure process new round event(last tc)
            if u = LeaderElection.get leader(Pacemaker.current round) then
                            // Leader code:  generate proposal.
            b ← Block-Tree.generate block( MemPool.get transactions(), Pacemaker.current  round )
            broadcast ProposalMsg⟨b,lasttc,Block-Tree.highcommitqc⟩

        """
