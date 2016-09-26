from collections import defaultdict

def combine():
    print 'start'
    
    #Read in phrases
    with open('phrases_with_alignments.txt', 'r') as phrase_file: 
        input_lines = phrase_file.readlines() 
    print 'read input'
    
    #Generate freq dictionaries
    dictF ={}
    dictE ={}
    dictFE={}
    for line in input_lines:
        f,e, freqs, alignments = line.split(" ||| ")
        #print f,len(f)
        freq_f, freq_e, freq_f_e = freqs.split()
        #print prob_f,prob_e,prob_f_e
        dictF[f]=freq_f
        dictE[e]=freq_e
        dictFE[(f,e)]=freq_f_e
        
    #REPLACE WITH ACTUAL OUTPUT FILE
    with open("kmo_output.txt") as kmo_file:
        kmo_lines = kmo_file.readlines()
    #Write frequencies behind kmo_output-line in new file
    with open("combine_output.txt","w") as combine_file:
        for kmo_line in kmo_lines[0:10]:
            #Possibly remove aligns, if they are not included in the actual KMO file
            f,e, probs,aligns = kmo_line.split(" ||| ")
            freq_f = dictF[f]
            freq_e = dictE[e]
            freq_f_e = dictFE[(f,e)]
            combine_file.write(kmo_line.rstrip() + " ||| " + freq_f +" "+ freq_e+" " + freq_f_e+"\n")
combine()