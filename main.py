from pacemaker import Pacemaker
from blocktree import BlockTree
from treeutility import TreeUtility
from ledger import Ledger
from LeaderElection import LeaderElection
from mempool import Mempool
class Main:

    #wait for next event and call start_event_processing()

    # init pacemaker, block tree ,ledger

    def __init__(self):
        self.block_tree = TreeUtility()
        self.ledger = Ledger()
        self.pacemaker = Pacemaker()
        self.mempool = Mempool()

    def start_event_processing(self,message,current_round, leader,f):
        if message=='local_time_out':
            Pacemaker.local_timeout_round()
        if message=='proposal_message':
            self.process_proposal_message(message,current_round,leader)
        if message=='vote message':
            self.process_vote_message(message)
        if message=='timeout message':
            self.process_timeout_message(message,f)

    def process_certificate_qc(self,qc):
        BlockTree.process_qc(qc)
        leader_election.update_leaders(qc)
        Pacemaker.advance_round_qc(qc.vote_info.round)

    def process_proposal_message(self,p,current_round,leader):
        self.process_certificate_qc(p.block.qc)
        self.process_certificate_qc(p.high_commit)
        Pacemaker.advance_round_tc(p.last_round_tc)
        round = Pacemaker.current_round

        leader =leader_election.get_leader(current_round)
        if p.block.round!=round or p.sender!=leader or p.author!=leader:
            return
        BlockTree.execute_and_insert(p)
        vote_msg = safety.make_vote(p.block,p.last_round_tc)
        if vote_msg:
            send(vote_msg,to=leader_election.get_leader(current_round + 1))

    def process_timeout_message(self,m,f):
        self.process_certificate_qc(m.tmo_info.high_qc)
        self.process_certificate_qc(m.high_commit_qc)
        Pacemaker.advance_round_tc(p.last_round_tc)
        tc = Pacemaker.process_remote_timeout(m,f)
        if tc:
            Pacemaker.advance_round(tc)
            self.process_new_round_event(tc)

    def process_vote_message(self,m):
        qc = BlockTree.process_vote(m)
        if qc:
            self.process_certificate_qc(qc)
            self.process_new_round_event(None)
    
    def process_new_round_event(last_tc):
        if leader_election.get_leader(pacemaker.current_round):
            b = block_tree.generate_block(mempool.get_transactions(),Pacemaker.current_round)
            #add author of block

            broadcast()
            """
            *
            *
            *
            """


        


    