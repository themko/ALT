from collections import defaultdict

def phrase_extraction():
    print 'start'
    with open('file.en', 'r') as e: #open the file
        en = e.readlines()
    with open('file.de', 'r') as d: #open the file
        de = d.readlines()     
    with open('file.aligned', 'r') as a: #open the file
        al = a.readlines()     
    
    phrases_e = defaultdict(int)
    phrases_f = defaultdict(int)
    phrases_f_e = defaultdict(int)
    
    #Extract phrases
    for eng,deu,aligns in zip(en,de,al):
        eng_words = eng.split()
        deu_words = deu.split()
        splitaligns = aligns.split()
        alignDictFE = defaultdict(list)
        alignDictEF = defaultdict(list) 
        for ali in splitaligns:
            ali_pair = (tuple(ali.split('-')))
            f_pos = int(ali_pair[0])
            e_pos = int(ali_pair[1])
            alignDictFE[f_pos].append(e_pos)
            alignDictEF[e_pos].append(f_pos)
            
        phrases = []
        #TODO: 2 for loops perhapse too costly...
        for en_ind in range(0,len(eng_words)):
            for cur_en_ind in range(en_ind,len(eng_words)):
                # Generate English candidate phrases by looking at all consecutive sequences
                candidate_phrase_en = range(en_ind,cur_en_ind+1)
                candidate_phrase_de = []
                de_to_en_align = []
                # Generate foreign candidate phrase based on
                # all alignment links of the English candidate phrase
                for pos in candidate_phrase_en:
                    candidate_phrase_de += alignDictEF[pos]
                #Check if if alignment-link exists
                if len(candidate_phrase_de) > 0:
                    candidate_phrase_de =  list(set(candidate_phrase_de))
                    # Look at alignments links of foreign phrase
                    for pos in candidate_phrase_de:
                        de_to_en_align += alignDictFE[pos]
                    de_to_en_align = list(set(de_to_en_align))
                    len_check = candidate_phrase_en + de_to_en_align
                    # Check if there are no links to English words
                    # outside the English candidate phrase
                    if len(set(len_check))<= len(candidate_phrase_en):
                        phrase_en = ""
                        phrase_de = ""
                        for pos in candidate_phrase_en:
                            phrase_en += eng_words[pos] + " "
                        phrase_en = phrase_en.rstrip()
                        for pos in candidate_phrase_de:
                            phrase_de += deu_words[pos] + " "
                        phrase_de = phrase_de.rstrip()
                        phrases_e[phrase_en] += 1
                        phrases_f[phrase_de] += 1
                        phrases_f_e[(phrase_de,phrase_en)] += 1
    #double-check output!!  
    phrases_file = open("phrases.txt","w")
    for f,e in phrases_f_e:
        phrases_file.write(f + " ||| " + e + " ||| " +  str(phrases_f[f]) + " " + str(phrases_e[e]) + " " + str(phrases_f_e[(f,e)]) + "\n")
    phrases_file.close()

phrase_extraction()
