class Main(process):

    #wait for next event and call start_event_processing()

    def start_event_processing(message):
        if message==local time out:
            pacemaker.local_timeout_round()
        if message==proposal message:
            process_proposal_message(message)
        if message==vote message:
            process_vote_message(message)
        if message==timeout message(message)

    def process_certificate_qc(qc):
        block_tree.process_qc(qc)
        leader_election.update_leaders(qc)
        pacemaker.advance_round(qc['vote_info']['round'])

    def process_proposal_message(p):
        process_certificate_qc(p['block']['qc'])
        process_certificate_qc(p['high_commit'])
        pacemeaker.advance_round_tc(p['last_round_tc'])
        round = pacemaker.current_round
        leader =leader_election.get_leader(current_round)
        if p['block']['round']!=round or p['sender']!=leader or p['author']!=leader:
            return
        block_tree.execute_and_insert(p)
        vote_msg = safety.make_vote(p['block'],p['last_round_tc'])
        if vote_msg:
            send(vote_msg,to=leader_election.get_leader(current_round + 1))

    def process_timeout_message(m):
        process_certificate_qc(m['tmo_info']['high_qc'])
        process_certificate_qc(m['high_commit_qc'])
        pacemeaker.advance_round_tc(p['last_round_tc'])
        tc = pacemaker.process_remote_timeout(m)
        if tc:
            pacemaker.advance_round(tc)
            process_new_round_event(tc)

    def process_vote_message(m):
        qc = block_tree.process_vote(m)
        if qc:
            process_certificate_qc(qc)
            process_new_round_event(None)
    
    def process_new_round_event(last_tc):
        if leader_election.get_leader(pacemaker.current_round):
            b = block_tree.generate_block(mempool.get_transactions(),pacemaker.current_round)

            broadcast()
            """
            *
            *
            *
            """


        


    