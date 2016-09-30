from collections import defaultdict

def reordering_estimates():
    print 'start'
    with open('file.en', 'r') as e_file: #open the file
        with open('file.de', 'r') as f_file: #open the file    
            with open('file.aligned', 'r') as a_file: #open the file
        
                phrases_e = defaultdict(int)
                phrases_f = defaultdict(int)
                phrases_f_e = defaultdict(int)
                alignments_f_e= {}
                #Extract phrases
                for e_line,f_line,al_line in zip(e_file,f_file,a_file)[0:1]:
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
                                break
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

##                    print f_line
##                    print e_line
##                    print "phrases per line:"
##                    for i in phrases_per_line:
##                        print i
##                    print
                    #Run through phrases left-to-right
                    #Foreach e check the f position of the next e (null=d, +1 m, -1= s)
##                    Are the really properly defined if several opptions exist, and we choice based on absences?
                    counterLR = 0
                    print e_line
                    #Run through all phrases of the e-sentence 
                    #len(e_line)
                    for phrases in phrases_per_line:
                        
                        #Check all phrases with this starting position
                        
                phrases_file = open("reorder_est.txt","w")
                print "Writing phrases to file..."
                for f,e in phrases_f_e:
                    phrases_file.write(f + " ||| " + e + " ||| " +  str(phrases_f[f]) + " " + str(phrases_e[e]) + " " + str(phrases_f_e[(f,e)]) + "\n")
                phrases_file.close()
    

reordering_estimates()
