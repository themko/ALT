from collections import defaultdict

def combine():
    print 'start'
    
    #Read in phrases
    dictF ={}
    dictE ={}
    dictFE={}
    with open('phrases_with_alignments.txt', 'r') as phrase_file:
        print "Reading phrases file..."
        for line in phrase_file:
            #Generate freq dictionaries
            f,e, freqs, alignments = line.split(" ||| ")
            f = f.strip()
            e = e.strip()
            #print f,len(f)
            freq_f, freq_e, freq_f_e = freqs.split()
            #print prob_f,prob_e,prob_f_e
            dictF[f]=freq_f
            dictE[e]=freq_e
            dictFE[(f,e)]=freq_f_e
        
    print "Now writing to file..."
    #REPLACE WITH ACTUAL OUTPUT FILE
    with open("lexical_weights_with_alignments.txt") as kmo_file:
        #Write frequencies behind kmo_output-line in new file
        with open("combine_output.txt","w") as combine_file:
            for kmo_line in kmo_file:
                #Possibly remove aligns, if they are not included in the actual KMO file
                f,e, probs,aligns = kmo_line.split(" ||| ")
                f = f.strip()
                e = e.strip()
                probs = probs.strip()
                freq_f = dictF[f]
                freq_e = dictE[e]
                freq_f_e = dictFE[(f,e)]
                combine_file.write(f + " ||| " + e + " ||| " + probs + " ||| " + freq_f + " " + freq_e + " "+ freq_f_e+"\n")
combine()
