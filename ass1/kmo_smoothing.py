from collections import defaultdict

def kmo_smoothing():
    print 'start'
    
    with open('file.en', 'r') as e: #open the file
        en = e.readlines()
    with open('file.de', 'r') as d: #open the file
        de = d.readlines()     
    with open('file.aligned', 'r') as a: #open the file
        al = a.readlines()     
    
    count_e = defaultdict(int)
    count_f = defaultdict(int)
    count_f_e = defaultdict(int)
    
    with open('file.en', 'r') as e_file: #open the file
        e_lines = e_file.readlines()
    with open('file.de', 'r') as f_file: #open the file
        f_lines = f_file.readlines()     
    with open('file.aligned', 'r') as a_file: #open the file
        al_lines = a_file.readlines()     
    
    count_e = defaultdict(int)
    count_f = defaultdict(int)
    count_f_e = defaultdict(int)
    
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
            
    
    
    
    with open('transition_probs.txt', 'r') as probs_file: #open the file
        probs = probs_file.readlines() 
    for line in probs:
        f,e, probs = line.split("|||")
        prob_f_given_e, prob_e_given_f = probs.split()
        print f
        print e
        print prob_f_given_e
        print prob_e_given_f

kmo_smoothing()
