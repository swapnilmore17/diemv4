from pacemaker import Pacemaker
from blocktree import BlockTree
class Main:

    #wait for next event and call start_event_processing()

    def start_event_processing(self,message,current_round, leader):
        if message=='local_time_out':
            Pacemaker.local_timeout_round()
        if message=='proposal_message':
            self.process_proposal_message(message,current_round,leader)
        if message=='vote message':
            self.process_vote_message(message)
        if message=='timeout message':
            self.process_timeout_message(message)

    def process_certificate_qc(self,qc):
        BlockTree.process_qc(qc)
        leader_election.update_leaders(qc)
        Pacemaker.advance_round(qc.vote_info.round)

    def process_proposal_message(self,p,current_round,leader):
        self.process_certificate_qc(p.block.qc)
        self.process_certificate_qc(p.high_commit)
        Pacemaker.advance_round_tc(p['last_round_tc'])
        round = Pacemaker.current_round

        leader =leader_election.get_leader(current_round)
        if p.block.round!=round or p.sender!=leader or p['author']!=leader:
            return
        BlockTree.execute_and_insert(p)
        vote_msg = safety.make_vote(p['block'],p['last_round_tc'])
        if vote_msg:
            send(vote_msg,to=leader_election.get_leader(current_round + 1))

    def process_timeout_message(self,m):
        self.process_certificate_qc(m.tmo_info.high_qc)
        self.process_certificate_qc(m.high_commit_qc)
        Pacemaker.advance_round_tc(p.last_round_tc)
        tc = Pacemaker.process_remote_timeout(m)
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
            b = block_tree.generate_block(mempool.get_transactions(),pacemaker.current_round)
            #add author of block

            broadcast()
            """
            *
            *
            *
            """


        


    