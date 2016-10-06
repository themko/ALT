from collections import defaultdict

WORD_BASED_ON = True

ORIENTATION_LR = 0
ORIENTATION_RL = 1

def get_phrases_transitions(phrases_list,f_phrase_with_positions,e_phrase_with_positions, monotone, swap, discontinuous_left, discontinuous_right, fe_pairs, orientation):
    f_phrase = f_phrase_with_positions[0]
    begin_f_phrase = f_phrase_with_positions[1]
    end_f_phrase = f_phrase_with_positions[2]
    e_phrase = e_phrase_with_positions[0]
    ## Because even if the next/previous phrases in phrase lists are empty, you still count the word
    if len(phrases_list)==0:
        print 'bailout'
        fe_pairs[(f_phrase,e_phrase)]+=1
    if orientation == ORIENTATION_LR:
        for phrase in phrases_list:
            #print 'next e_phrase', phrase
            ##
            fe_pairs[(f_phrase,e_phrase)]+=1
            begin_f_next_phrase = phrase[0][1]
            end_f_next_phrase = phrase[0][2]
            #Check for monotone,swap,discontinuous
            if(begin_f_next_phrase == end_f_phrase +1):
                #print 'LR monotone'
                monotone[(f_phrase,e_phrase)] +=1
            elif(end_f_next_phrase == begin_f_phrase -1):
                # Old: elif(begin_f_phrase == end_f_next_phrase+1):
                #print 'LR swap'
                swap[(f_phrase,e_phrase)] +=1
            elif(end_f_next_phrase < begin_f_phrase):
                #print 'LR discontinuous left'
                discontinuous_left[(f_phrase,e_phrase)] +=1
            elif(begin_f_next_phrase > end_f_phrase):
                #print 'LR discontinuous right'
                discontinuous_right[(f_phrase,e_phrase)] +=1
            else:
                print "Unknown transition LR"
    else:
        for phrase in phrases_list:
            #print 'previous e_phrase', phrase
            ##
            fe_pairs[(f_phrase,e_phrase)]+=1
            #print f_phrase, e_phrase, fe_pairs[(f_phrase,e_phrase)]
            begin_f_previous_phrase = phrase[0][1]
            end_f_previous_phrase = phrase[0][2]
            
            #Check conditions
            if(end_f_previous_phrase == begin_f_phrase -1):
                #print 'RL monotone'
                monotone[(f_phrase,e_phrase)] +=1
            # Old: elif(end_f_previous_phrase == begin_f_phrase +1):
            elif(begin_f_previous_phrase == end_f_phrase +1):
                #print 'RL swap'
                swap[(f_phrase,e_phrase)] +=1
            elif (end_f_previous_phrase < begin_f_phrase):
                #print 'RL discontinuous left'
                discontinuous_left[(f_phrase,e_phrase)] +=1
            elif (begin_f_previous_phrase > end_f_phrase):
                #print 'RL discontinuous right'
                discontinuous_right[(f_phrase,e_phrase)] +=1
            else:
                print "Unknown transition RL"


def reordering_estimates():
    print 'start'
    with open('file.en', 'r') as e_file: #open the file
        with open('file.de', 'r') as f_file: #open the file    
            with open('file.aligned', 'r') as a_file: #open the file
                phrases_e = defaultdict(int)
                phrases_f = defaultdict(int)
                phrases_f_e = defaultdict(int)
                
                # Dicts for phrase-based reordering
                LR_fe_pairs = defaultdict(int)
                RL_fe_pairs = defaultdict(int)
                monotone_LR = defaultdict(int)
                swap_LR = defaultdict(int)
                discontinuous_left_LR = defaultdict(int)
                discontinuous_right_LR = defaultdict(int)
                monotone_RL = defaultdict(int)
                swap_RL = defaultdict(int)
                discontinuous_left_RL = defaultdict(int)
                discontinuous_right_RL = defaultdict(int) 
                
                # Dicts for word-based reordering
                LR_fe_pairs_word = defaultdict(int)
                RL_fe_pairs_word = defaultdict(int)
                monotone_word_LR = defaultdict(int)
                swap_word_LR = defaultdict(int)
                discontinuous_word_left_LR = defaultdict(int)
                discontinuous_word_right_LR = defaultdict(int)
                monotone_word_RL = defaultdict(int)
                swap_word_RL = defaultdict(int)
                discontinuous_word_left_RL = defaultdict(int)   
                discontinuous_word_right_RL = defaultdict(int)   
                
                alignments_f_e= {}
                #Extract phrases
                for e_line,f_line,al_line in zip(e_file,f_file,a_file)[5:6]:
                    phrases_per_line_start = defaultdict(list)
                    phrases_per_line_end = defaultdict(list)
                    e_words = e_line.split()
                    f_words = f_line.split()
                    al_pairs = al_line.split()
                    alignDictFE = defaultdict(list)
                    alignDictEF = defaultdict(list) 
                    for ali in al_pairs:
                        ali_pair = (tuple(ali.split('-')))
                        f_pos = int(ali_pair[0])
                        e_pos = int(ali_pair[1])
                        # Save alignment links to dictionaries, in two directions
                        alignDictFE[f_pos].append(e_pos)
                        alignDictEF[e_pos].append(f_pos)
                        
                    phrases = []
                    for e_ind in range(0,len(e_words)):
                        for cur_e_ind in range(e_ind,len(e_words)):
                            # Generate English candidate phrases, by looking at all
                            # consecutive sequences of English words.
                            candidate_phrase_e = range(e_ind,cur_e_ind+1)
                            #Disregard phrases longer than 7
                            if len(candidate_phrase_e)>7:
                                continue
                            candidate_phrase_f = []
                            f_to_e_align = []
                            # Generate foreign candidate phrase based on
                            # all alignment links of the English candidate phrase
                            for pos in candidate_phrase_e:
                                candidate_phrase_f += alignDictEF[pos]
                            # Check if there are any alignment links
                            if candidate_phrase_f != []:
                                # We take the whole range, so also unaligned positions
                                # in between
                                candidate_phrase_f = range(min(candidate_phrase_f),max(candidate_phrase_f)+1)
                                #Disregard phrases longer than 7
                                if len(candidate_phrase_f)>7:
                                    break
                                # Look at alignments links of foreign candidate phrase
                                for pos in candidate_phrase_f:
                                    f_to_e_align += alignDictFE[pos]
                                f_to_e_align = list(set(f_to_e_align))
                                len_check = candidate_phrase_e + f_to_e_align
                                # Check if there are no links to English words
                                # outside the English candidate phrase
                                if len(set(len_check))<= len(candidate_phrase_e):
                                    # Phrase pair accepted as valid
                                    phrase_e = ""
                                    phrase_f = ""
                                    for pos in candidate_phrase_e:
                                        phrase_e += e_words[pos] + " "
                                        
                                    phrase_e = phrase_e.rstrip()
                                    for pos in candidate_phrase_f:
                                        phrase_f += f_words[pos] + " "
                                    
                                    phrase_f = phrase_f.rstrip()
                                    # Keep track of counts
                                    phrases_e[phrase_e] += 1
                                    phrases_f[phrase_f] += 1
                                    phrases_f_e[(phrase_f,phrase_e)] += 1
                                    f1,f2 = candidate_phrase_f[0], candidate_phrase_f[-1]
                                    e1,e2 = candidate_phrase_e[0], candidate_phrase_e[-1]
                                    #Indexed based on e-phrase indices
                                    phrases_per_line_start[(e1)].append(((phrase_f,f1,f2),(phrase_e,e1,e2)))
                                    phrases_per_line_end[(e2)].append(((phrase_f,f1,f2),(phrase_e,e1,e2)))

                    #print f_line.strip()
                    #print e_line.rstrip()
                    #Run through all phrases of the e-sentence 
                    #print
                    print "L->R:"
                    #Iterate L->R over starting positiong of e-phrases
                    for start_pos_e in phrases_per_line_start:
                        phrases_list = phrases_per_line_start[start_pos_e]
                        for start_pos_phrase in phrases_list:
                            
                            #print 'start_pos_e',start_pos_e,'phrases:',start_pos_phrase
                            f_phrase_with_positions = start_pos_phrase[0]
                            e_phrase_with_positions = start_pos_phrase[1]
                            f_phrase = start_pos_phrase[0][0]
                            e_phrase = start_pos_phrase[1][0]
                            #Check all phrases with this starting position
                            #For english phrases check next position
                            end_e_phrase = start_pos_phrase[1][2]
                            begin_e_phrase = start_pos_phrase[1][1]
                            end_f_phrase = start_pos_phrase[0][2]
                            begin_f_phrase = start_pos_phrase[0][1]
                            
                            #Ignore l->r checks for e-phrases at the end of the sentence
                            if(end_e_phrase+1 not in phrases_per_line_start ):
                                #We assume that ends of sentences are monotone!
                                #and that unaligned words are neither monotone,swap or disc.
                                LR_fe_pairs[(f_phrase,e_phrase)]+=1
                                LR_fe_pairs_word[(f_phrase,e_phrase)]+=1
                                
                                #We assume then all positions are possible:
                                if(end_e_phrase == len(e_words)-1):
                                    #print 'end'
                                    monotone_LR[(f_phrase,e_phrase)] +=1
                                    monotone_word_LR[(f_phrase,e_phrase)] +=1
                            else:
                                # Phrase-based reordering probabilities
                                next_phrases_list = phrases_per_line_start[end_e_phrase +1]
                                # monotone,swap and discontinuous dicts are updated by method
                                get_phrases_transitions(next_phrases_list,f_phrase_with_positions,e_phrase_with_positions, monotone_LR, swap_LR, discontinuous_left_LR, discontinuous_right_LR, LR_fe_pairs, ORIENTATION_LR)
                                
                                # Word-based reordering probabilities
                                next_e_pos = end_e_phrase + 1
                                next_f_positions = alignDictEF[next_e_pos]
                                next_words_list = []
                                for next_f_pos in next_f_positions:
                                    f_word = f_words[next_f_pos]
                                    e_word = e_words[next_e_pos]
                                    # End and begin position of word are the same
                                    next_words_list.append(((f_word,next_f_pos,next_f_pos),(e_word,next_e_pos,next_e_pos)))
                                    
                                # monotone,swap and discontinuous dicts are updated by method
                                get_phrases_transitions(next_words_list,f_phrase_with_positions,e_phrase_with_positions, monotone_word_LR, swap_word_LR, discontinuous_word_left_LR, discontinuous_word_right_LR, LR_fe_pairs_word, ORIENTATION_LR)
                    
                    print
                    print "R->L:"
                    #Iterate R->L over end positiong of e-phrases
                    for end_pos_e in reversed(phrases_per_line_end.keys()):
                        phrases_list = phrases_per_line_end[end_pos_e]
                        for end_pos_phrase in phrases_list:
                            #print 'end_pos_e',end_pos_e,'phrases:',end_pos_phrase
                            f_phrase_with_positions = end_pos_phrase[0]
                            e_phrase_with_positions = end_pos_phrase[1]
                            f_phrase = end_pos_phrase[0][0]
                            e_phrase = end_pos_phrase[1][0]
                            
                            #Check all phrases with this ending position
                            #For english phrases check next position
                            end_e_phrase = end_pos_phrase[1][2]
                            begin_e_phrase = end_pos_phrase[1][1]
                            end_f_phrase = end_pos_phrase[0][2]
                            begin_f_phrase =end_pos_phrase[0][1]
                            #Ignore l-r checks for e-phrases at the end of the sentence

                            #Count the number of times the fe pair occurs in RL sentences
                            #For instance in cases where there is no non-overlapping phrase before the start of the sentence
                            if(begin_e_phrase-1 not in phrases_per_line_end.keys() ):
                            #We assume beginnings of sentences are RL monotone
                            #and that unaligned words are neither monotone,swap or disc.
                                RL_fe_pairs[(f_phrase,e_phrase)]+=1
                                RL_fe_pairs_word[(f_phrase,e_phrase)]+=1
                                if(begin_e_phrase == 0):
                                    #print 'begin'
                                    monotone_RL[(f_phrase,e_phrase)] +=1
                                    monotone_word_RL[(f_phrase,e_phrase)] +=1

                            else:
                                # Phrase-based reordering probabilities
                                prev_phrases_list = phrases_per_line_end[begin_e_phrase -1]
                                #print prev_phrases_list
                                get_phrases_transitions(prev_phrases_list,f_phrase_with_positions,e_phrase_with_positions, monotone_RL, swap_RL, discontinuous_left_RL, discontinuous_right_RL, RL_fe_pairs, ORIENTATION_RL)
                                
                                # Word-based reordering probabilities
                                prev_e_pos = begin_e_phrase - 1
                                prev_f_positions = alignDictEF[prev_e_pos]
                                prev_words_list = []
                                for prev_f_pos in prev_f_positions:
                                    f_word = f_words[prev_f_pos]
                                    e_word = e_words[prev_e_pos]
                                    # End and begin position of word are the same
                                    prev_words_list.append(((f_word,prev_f_pos,prev_f_pos),(e_word,prev_e_pos,prev_e_pos)))
                                    
                                # monotone,swap and discontinuous dicts are updated by method
                                get_phrases_transitions(prev_words_list,f_phrase_with_positions,e_phrase_with_positions, monotone_word_RL, swap_word_RL, discontinuous_word_left_RL, discontinuous_word_right_RL, RL_fe_pairs_word, ORIENTATION_RL)
                            #print 'current',f_phrase,e_phrase,'counter',RL_fe_pairs_word[(',',',')]

                print "Writing phrases to file..."
                # Write phrase-based reordering probabilities to phrase_file
                with open("reorder_est.txt","w") as phrases_file:
                    for f,e in phrases_f_e.iterkeys():
                        # Phrase-based reordering
                        p_m_LR = 1.*monotone_LR[f,e]/LR_fe_pairs[(f,e)]
                        #print 'pmlr', p_m_LR
                        p_d_left_LR = 1.*discontinuous_left_LR[f,e]/LR_fe_pairs[(f,e)]
                        p_d_right_LR = 1.*discontinuous_right_LR[f,e]/LR_fe_pairs[(f,e)]
                        p_s_LR = 1.*swap_LR[f,e]/LR_fe_pairs[(f,e)]
                        #REMEMBER disc left & right!!
                        #print 'fe ',f,e,RL_fe_pairs[(f,e)]

                        p_m_RL = 1.* monotone_RL[(f,e)]/RL_fe_pairs[(f,e)]
                        p_s_RL = 1.*swap_RL[f,e]/RL_fe_pairs[(f,e)]
                        p_d_left_RL = 1.*discontinuous_left_RL[f,e]/RL_fe_pairs[(f,e)]
                        p_d_right_RL = 1.*discontinuous_right_RL[f,e]/RL_fe_pairs[(f,e)]

                        phrases_file.write(f + " ||| " + e + " ||| " +  str(p_m_LR) + " " + str(p_s_LR )+ " " +str(p_d_left_LR) + " "+str(p_d_right_LR) + " " +str(p_m_RL )+ " " + str(p_s_RL) + " " + str(p_d_left_RL)+" " + str(p_d_right_RL)+"\n")
                
                print 'Writing words to file'
                # Write word-based reordering probabilities to file
                with open("reorder_est_wordbased.txt","w") as phrases_file_wordbased:
                    for f,e in phrases_f_e.iterkeys():
                        # Word-based reordering
                        p_m_LR = 1.*monotone_word_LR[f,e]/LR_fe_pairs_word[(f,e)]
                        #print 'pmlr', p_m_LR
                        p_d_left_LR = 1.*discontinuous_word_left_LR[f,e]/LR_fe_pairs_word[(f,e)]
                        p_d_right_LR = 1.*discontinuous_word_right_LR[f,e]/LR_fe_pairs_word[(f,e)]
                        p_s_LR = 1.*swap_word_LR[f,e]/LR_fe_pairs_word[(f,e)]
                        #REMEMBER disc left & right!!
                        #print 'fe ',f,e,RL_fe_pairs_word[(f,e)]
                        p_m_RL = 1.* monotone_word_RL[(f,e)]/RL_fe_pairs_word[(f,e)]
                        p_s_RL = 1.*swap_word_RL[f,e]/RL_fe_pairs_word[(f,e)]
                        p_d_left_RL = 1.*discontinuous_word_left_RL[f,e]/RL_fe_pairs_word[(f,e)]
                        p_d_right_RL = 1.*discontinuous_word_right_RL[f,e]/RL_fe_pairs_word[(f,e)]
                        phrases_file_wordbased.write(f + " ||| " + e + " ||| " +  str(p_m_LR) + " " + str(p_s_LR )+ " " +str(p_d_left_LR) + " " +str(p_d_right_LR) + " "+str(p_m_RL )+ " " + str(p_s_RL) + " " + str(p_d_left_RL)+" " + str(p_d_right_RL)+"\n")
                    
    

reordering_estimates()
