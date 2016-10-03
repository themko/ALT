from collections import defaultdict

def reordering_estimates():
    print 'start'
    with open('file.en', 'r') as e_file: #open the file
        with open('file.de', 'r') as f_file: #open the file    
            with open('file.aligned', 'r') as a_file: #open the file
                phrases_e = defaultdict(int)
                phrases_f = defaultdict(int)
                phrases_f_e = defaultdict(int)
                
                monotone_LR = defaultdict(int)
                swap_LR = defaultdict(int)
                discontinuous_LR = defaultdict(int)
                
                monotone_RL = defaultdict(int)
                swap_RL = defaultdict(int)
                discontinuous_RL = defaultdict(int)      
                          
                alignments_f_e= {}
                #Extract phrases
                for e_line,f_line,al_line in zip(e_file,f_file,a_file)[5:6]:
                    phrases_per_line_start = {}
                    phrases_per_line_end = {}
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
                                    phrases_per_line_start[(e1)] = ((phrase_f,f1,f2),(phrase_e,e1,e2))
                                    phrases_per_line_end[(e2)] = ((phrase_f,f1,f2),(phrase_e,e1,e2))

##                    Are the really properly defined if several options exist, and we choice based on absences?
                    print f_line.strip()
                    print e_line.rstrip()
                    #Run through all phrases of the e-sentence 
                    print
                    print "L->R:"
                    #Iterate L->R over starting positiong of e-phrases
                    for start_pos_e in phrases_per_line_start.keys():
                        print 'start_pos_e',start_pos_e,'phrases:',phrases_per_line_start[start_pos_e]
                        f_word = phrases_per_line_start[start_pos_e][0][0]
                        e_word = phrases_per_line_start[start_pos_e][1][0]
                        #Check all phrases with this starting position
                        #NOT NECESSARY IN FEW EXAMMPLES ALL KEYS UNIQUE ENTRIES, MIGHT CHANGE!!
                        
                        #For english phrases check next position
                        end_e_phrase = (phrases_per_line_start[start_pos_e][1][2])
                        begin_e_phrase = (phrases_per_line_start[start_pos_e][1][1])
                        end_f_phrase = (phrases_per_line_start[start_pos_e][0][2])
                        begin_f_phrase = (phrases_per_line_start[start_pos_e][0][1])
                        #Ignore l-r checks for e-phrases at the end of the sentence
                        if(end_e_phrase == len(e_words)-1):
                            print 'end of sentence'
                            continue
                        #What is next e-row is empty?? 
                        if(end_e_phrase+1 not in phrases_per_line_start.keys() ):
                            print 'EMPTY'
                            continue
                        print 'next e_phrase', phrases_per_line_start[end_e_phrase +1]
                        #IS THIS WORKING PROPERLY?
                        begin_f_next_phrase = phrases_per_line_start[end_e_phrase +1][0][1]
                        end_f_next_phrase = phrases_per_line_start[end_e_phrase +1][0][2]
                        #Check for monotone,swap,discontinuous
                        if(begin_f_next_phrase == end_f_phrase +1):
                            print 'LR monotone'
                            monotone_LR[(f_word,e_word)] +=1
                        elif(begin_f_phrase == end_f_next_phrase+1):
                            print 'LR swap'
                            swap_LR[(f_word,e_word)] +=1
                        else:
                            print 'LR discontinuous'
                            discontinuous_LR[(f_word,e_word)] +=1
                        print
                    
                    print
                    print "R->L:"
                    ##THIS STILL NOT WORKING PROPERLY
                    #Iterate R->L over end positiong of e-phrases
                    for end_pos_e in reversed(phrases_per_line_end.keys()):
                        print 'end_pos_e',end_pos_e,'phrases:',phrases_per_line_end[end_pos_e]
                        f_word = phrases_per_line_end[end_pos_e][0][0]
                        e_word = phrases_per_line_end[end_pos_e][1][0]
                        #Check all phrases with this ending position
                        #NOT NECESSARY IN FEW EXAMMPLES ALL KEYS UNIQUE ENTRIES, MIGHT CHANGE!!
                        
                        #For english phrases check next position
                        end_e_phrase = (phrases_per_line_end[end_pos_e][1][2])
                        begin_e_phrase = (phrases_per_line_end[end_pos_e][1][1])
                        end_f_phrase = (phrases_per_line_end[end_pos_e][0][2])
                        begin_f_phrase = (phrases_per_line_end[end_pos_e][0][1])
                        #Ignore l-r checks for e-phrases at the end of the sentence
                        if(begin_e_phrase == 0):
                            print 'start of sentence'
                            continue
                        #What is next e-row is empty?? 
                        #For instance in cases where there is no non-overlapping phrase before the start of the sentence
                        if(end_e_phrase-1 not in phrases_per_line_end.keys() ):
                            print 'EMPTY'
                            continue
                        print 'previous e_phrase', phrases_per_line_end[begin_e_phrase -1]
                        ###DOUBLE CHECK THESE
                        begin_f_previous_phrase = phrases_per_line_end[end_e_phrase -1][0][1]
                        end_f_previous_phrase = phrases_per_line_end[end_e_phrase -1][0][2]
                        
                        ###NDOUBLE-CHECK NEW CONDITIONS
                        #Check conditions
                        if(end_f_previous_phrase == begin_f_phrase -1):
                            print 'RL monotone'
                            monotone_RL[(f_word,e_word)] +=1
                        elif(begin_f_phrase == end_f_previous_phrase-1):
                            print 'RL swap'
                            swap_RL[(f_word,e_word)] +=1
                        else:
                            print 'RL discontinuous'
                            discontinuous_RL[(f_word,e_word)] +=1
                        print
                print 'mono',monotone_LR, monotone_RL
                phrases_file = open("reorder_est.txt","w")
                print "Writing phrases to file..."
                for f,e in phrases_f_e:
                    phrases_file.write(f + " ||| " + e + " ||| " +  str(phrases_f[f]) + " " + str(phrases_e[e]) + " " + str(phrases_f_e[(f,e)]) + "\n")
                phrases_file.close()
    

reordering_estimates()
