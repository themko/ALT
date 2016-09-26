from collections import defaultdict

def phrase_extraction():
    print 'start'
    with open('file.en', 'r') as e_file: #open the file
        e_lines = e_file.readlines()
    with open('file.de', 'r') as f_file: #open the file
        f_lines = f_file.readlines()     
    with open('file.aligned', 'r') as a_file: #open the file
        al_lines = a_file.readlines()     
    
    phrases_e = defaultdict(int)
    phrases_f = defaultdict(int)
    phrases_f_e = defaultdict(int)
    alignments_f_e= {}
    #Extract phrases
    for e_line,f_line,al_line in zip(e_lines,f_lines,al_lines):
        e_words = e_line.split()
        f_words = f_line.split()
        al_pairs = al_line.split()
        alignDictFE = defaultdict(list)
        alignDictEF = defaultdict(list) 
        for ali in al_pairs:
            ali_pair = (tuple(ali.split('-')))
            f_pos = int(ali_pair[0])
            e_pos = int(ali_pair[1])
            alignDictFE[f_pos].append(e_pos)
            alignDictEF[e_pos].append(f_pos)
            
        phrases = []
        #TODO: 2 for loops perhapse too costly...
        for e_ind in range(0,len(e_words)):
            for cur_e_ind in range(e_ind,len(e_words)):
                # Generate English candidate phrases by looking at all consecutive sequences
                candidate_phrase_e = range(e_ind,cur_e_ind+1)
                candidate_phrase_f = []
                f_to_e_align = []
                # Generate foreign candidate phrase based on
                # all alignment links of the English candidate phrase
                for pos in candidate_phrase_e:
                    candidate_phrase_f += alignDictEF[pos]
                #We fill in the positions between alignments 
                #print 'cpf_pre', candidate_phrase_f
                if candidate_phrase_f != []:
                    candidate_phrase_f = range(min(candidate_phrase_f),max(candidate_phrase_f)+1)
                    #print 'cpf',candidate_phrase_f
                
                    # Look at alignments links of foreign phrase
                    #print candidate_phrase_f
                    for pos in candidate_phrase_f:
                        f_to_e_align += alignDictFE[pos]
                    f_to_e_align = list(set(f_to_e_align))
                    len_check = candidate_phrase_e + f_to_e_align
                    # Check if there are no links to English words
                    # outside the English candidate phrase
                    if len(set(len_check))<= len(candidate_phrase_e):
                        phrase_e = ""
                        phrase_f = ""
                        for pos in candidate_phrase_e:
                            phrase_e += e_words[pos] + " "
                            
                        phrase_e = phrase_e.rstrip()
                        for pos in candidate_phrase_f:
                            phrase_f += f_words[pos] + " "
                        
                        phrase_f = phrase_f.rstrip()
                        phrases_e[phrase_e] += 1
                        phrases_f[phrase_f] += 1
                        phrases_f_e[(phrase_f,phrase_e)] += 1
                        
                        #Output te
                        f_start = candidate_phrase_f[0]
                        e_start = candidate_phrase_e[0]
                        new_alignments = []
                        for f_pos in candidate_phrase_f:
                            f_new = f_pos - f_start
                            for e_pos in alignDictFE[f_pos]:
                                e_new = e_pos - e_start
                                new_alignments.append((f_new,e_new))
                        alignments_f_e[(phrase_f,phrase_e)] = new_alignments
                        
    #double-check output!!  
    
#    phrases_file = open("phrases.txt","w")
#    for f,e in phrases_f_e:
#        phrases_file.write(f + " ||| " + e + " ||| " +  str(phrases_f[f]) + " " + str(phrases_e[e]) + " " + str(phrases_f_e[(f,e)]) + "\n")
#    phrases_file.close()

    phrases_file = open("phrases_with_alignments.txt","w")
    for f,e in phrases_f_e:
        alignments_string = ""
        for pair in alignments_f_e[(f,e)]:
            alignments_string += str(pair[0]) + "-" + str(pair[1]) + " "
        phrases_file.write(f + " ||| " + e + " ||| " +  str(phrases_f[f]) + " " + str(phrases_e[e]) + " " + str(phrases_f_e[(f,e)]) + " ||| " + alignments_string + "\n")
    phrases_file.close()
    
phrase_extraction()
