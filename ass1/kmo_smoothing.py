from collections import defaultdict

def generate_word_translation_probabilities():
    print 'start'
    
    with open('file.en', 'r') as e_file: #open the file
        e_lines = e_file.readlines()
    with open('file.de', 'r') as f_file: #open the file
        f_lines = f_file.readlines()     
    with open('file.aligned', 'r') as a_file: #open the file
        al_lines = a_file.readlines()     
    
    count_e = defaultdict(int)
    count_f = defaultdict(int)
    count_f_e = defaultdict(int)
    
    # Count alignments
    for e_line,f_line,al_line in zip(e_lines,f_lines,al_lines)[:4000]:
        e_words = e_line.split()
        f_words = f_line.split()
        al_pairs = al_line.split()
        
        # Keep track of aligned words in both languages
        # to find unaligned words
        e_aligned = []
        f_aligned = []
        
        for ali in al_pairs:
            ali_pair = (tuple(ali.split('-')))
            f_pos = int(ali_pair[0])
            e_pos = int(ali_pair[1])
            e_word = e_words[e_pos]
            f_word = f_words[f_pos]
            e_aligned.append(e_pos)
            f_aligned.append(f_pos)
            
            count_e[e_word] +=1
            count_f[f_word] +=1
            count_f_e[(f_word,e_word)] += 1
        
        # Find unaligned words, align them to NULL, and add to count dictionary
        list_e = range(0,len(e_words))
        list_f = range(0,len(f_words))
        intersect_e_aligned = list(set(list_e) & set(e_aligned))
        e_unaligned = [i for i in list_e if i not in intersect_e_aligned]
        intersect_f_aligned = list(set(list_f) & set(f_aligned))
        f_unaligned = [i for i in list_f if i not in intersect_f_aligned]
        for pos in e_unaligned:
            e_word = e_words[pos]
            count_e[e_word] += 1
            count_f["NULL"] += 1
            count_f_e[("NULL",e_word)] +=1
        for pos in f_unaligned:
            f_word = f_words[pos]
            count_e["NULL"] += 1
            count_f[f_word] += 1
            count_f_e[(f_word,"NULL")] +=1
    
    w_f_given_e = defaultdict(int)
    w_e_given_f = defaultdict(int)
    for f,e in count_f_e:
        print f,e
        print count_f[f],count_e[e]
        w_f_given_e[(f,e)] = float(count_f_e[(f,e)]) / float(count_e[e])
        w_e_given_f[(e,f)] = float(count_f_e[(f,e)]) / float(count_f[f])
    #print sorted(w_f_given_e.items(), key=lambda item: item[1], reverse=True)[:100]
    return w_f_given_e, w_e_given_f
    
def print_lexical_weighting(w_f_given_e, w_e_given_f):
    with open('transition_probs_with_alignments.txt', 'r') as probs_file: #open the file
        probs = probs_file.readlines() 
    for line in probs:
        f,e, probs, alignments = line.split("|||")
        prob_f_given_e, prob_e_given_f = probs.split()
        print f
        print e
        print prob_f_given_e
        print prob_e_given_f
        
        # Read alignments
        alignDictFE = {}
        al_pairs = alignments.split()
        alignDictFE = defaultdict(list)
        alignDictEF = defaultdict(list) 
        for ali in al_pairs:
            ali_pair = (tuple(ali.split('-')))
            f_pos = int(ali_pair[0])
            e_pos = int(ali_pair[1])
            alignDictFE[f_pos].append(e_pos)
    
    
def kmo_smoothing():
    w_f_given_e, w_e_given_f = generate_word_translation_probabilities()
    print_lexical_weighting(w_f_given_e, w_e_given_f)
