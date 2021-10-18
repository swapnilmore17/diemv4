from pacemaker import Pacemaker
from blocktree import BlockTree
from treeutility import TreeUtility
from ledger import Ledger
from LeaderElection import LeaderElection
from mempool import Mempool
from datastructs import ProposalMsg
class Main:

    #wait for next event and call start_event_processing()

    def __init__(self):
        self.block_tree = TreeUtility()
        self.ledger = Ledger()
        self.pacemaker = Pacemaker(0,None,{})
        self.mempool=Mempool()
        self.leader_election = LeaderElection()

    #def start_event_processing(self,message,current_round, leader,f):

    def process_certificate_qc(self,qc):
        self.block_tree.process_qc(qc)
        self.leader_election.update_leaders(qc)
        self.pacemaker.advance_round_qc(qc.vote_info.round)

    def process_proposal_message(self,p,current_round):
        self.process_certificate_qc(p.block.qc)
        self.process_certificate_qc(p.high_commit)
        self.pacemaker.advance_round_tc(p.last_round_tc)
        round = self.pacemaker.current_round

        leader =self.leader_election.get_leader(current_round)
        if p.block.round!=round or p.sender!=leader or p.author!=leader:
            return None
        self.block_tree.execute_and_insert(p)
        vote_msg = self.safety.make_vote(p.block,p.last_round_tc)
        if vote_msg:
            next_leader = self.leader_election.get_leader(current_round + 1)
            return (vote_msg,next_leader)
        return None

    def process_timeout_message(self,m,f):
        self.process_certificate_qc(m.tmo_info.high_qc)
        self.process_certificate_qc(m.high_commit_qc)
        self.pacemaker.advance_round_tc(m.last_round_tc)
        tc = self.pacemaker.process_remote_timeout(m,f)
        if tc:
            self.pacemaker.advance_round(tc)
            msg = self.process_new_round_event(tc)
            return msg
        return None


    def process_vote_message(self,m):
        qc = self.block_tree.process_vote(m)
        if qc:
            self.process_certificate_qc(qc)
            msg = self.process_new_round_event(None)
            return msg
        return None
    
    def process_new_round_event(self,last_tc):
        if self.leader_election.get_leader(self.pacemaker.current_round):
            b = self.block_tree.generate_block(self.mempool.get_transactions(),self.pacemaker.current_round)
            #add author of block
            msg = ProposalMsg(b,last_tc,self.block_tree.high_commit_qc)
            return msg 
        return None


        


    