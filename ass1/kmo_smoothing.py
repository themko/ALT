from collections import defaultdict
import os
import cPickle as pickle

def generate_word_translation_probabilities():
    print 'Generating word translation probabilities...'
    w_f_given_e = {}
    w_e_given_f = {}
    if os.path.isfile("word_translation_probs.p"):
        print "File present, loading word translation probabilities from file..."
        with open("word_translation_probs.p","rb") as pickle_file:
            w_f_given_e, w_e_given_f = pickle.load(pickle_file)
    else:
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
        for e_line,f_line,al_line in zip(e_lines,f_lines,al_lines):
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
            w_f_given_e[(f,e)] = float(count_f_e[(f,e)]) / float(count_e[e])
            w_e_given_f[(e,f)] = float(count_f_e[(f,e)]) / float(count_f[f])
        #print sorted(w_f_given_e.items(), key=lambda item: item[1], reverse=True)[:100]
        
        # Save as pickle
        print "Saving word translation probabilities to file..."
        with open("word_translation_probs.p","wb") as pickle_file:
            pickle.dump((w_f_given_e, w_e_given_f), pickle_file)
    return w_f_given_e, w_e_given_f
    
def print_lexical_weighting(w_f_given_e, w_e_given_f):
    print "Calculating lexical weights..."
    with open('transition_probs_with_alignments.txt', 'r') as probs_file: #open the file
        with open('lexical_weights_with_alignments.txt','w') as lex_file:
            for line in probs_file:
                f,e, probs, alignments = line.split("|||")
                alignments = alignments.lstrip()
                prob_f_given_e, prob_e_given_f = probs.split()
                
                # Read alignments
                al_pairs = alignments.split()
                alignDictEF = defaultdict(list)
                alignDictFE = defaultdict(list) 
                for ali in al_pairs:
                    ali_pair = (tuple(ali.split('-')))
                    f_pos = int(ali_pair[0])
                    e_pos = int(ali_pair[1])
                    alignDictEF[e_pos].append(f_pos)
                    alignDictFE[f_pos].append(e_pos)
                
                # Calculate lexical weight lex(e|f)
                lex_e_f = float(1)
                e_words = e.split()
                f_words = f.split()
                e_positions = range(0,len(e_words))
                for e_pos in e_positions:
                    link_score = 0        
                    # If nothing linked on f side, align with NULL  
                    if e_pos not in alignDictEF:
                        e_word = e_words[e_pos]
                        #print "+w(" + str(e_word) + "|NULL): " + str(w_e_given_f[(e_word,"NULL")])
                        link_score += w_e_given_f[(e_word,"NULL")]
                    else:
                        options = alignDictEF[e_pos]
                        for f_pos in options:
                            e_word = e_words[e_pos]
                            f_word = f_words[f_pos]
                            link_score += w_e_given_f[(e_word,f_word)]
                            #print "+w(" + str(e_word) + "|" + str(f_word) + "): " + str(w_e_given_f[(e_word,f_word)])
                        # Divide link score by number of options
                        link_score *= 1/float(len(options))
                    #print "Link score: " + str(link_score)
                    lex_e_f *= link_score
                #print "Lex(e|f):" + str(lex_e_f)
                
                # Calculate lexical weight lex(f|e)
                lex_f_e = float(1)
                f_positions = range(0,len(f_words))
                for f_pos in f_positions:
                    link_score = 0        
                    # If nothing linked on e side, align with NULL  
                    #### TODO: Is this needed at this side?
                    if f_pos not in alignDictFE:
                        f_word = f_words[f_pos]
                        #print "+w(" + str(f_word) + "|NULL): " + str(w_f_given_e[(f_word,"NULL")])
                        link_score += w_f_given_e[(f_word,"NULL")]
                    else:
                        options = alignDictFE[f_pos]
                        for e_pos in options:
                            f_word = f_words[f_pos]
                            e_word = e_words[e_pos]
                            link_score += w_f_given_e[(f_word,e_word)]
                            #print "+w(" + str(f_word) + "|" + str(e_word) + "): " + str(w_f_given_e[(f_word,e_word)])
                        # Divide link score by number of options
                        link_score *= 1/float(len(options))
                    #print "Link score: " + str(link_score)
                    lex_f_e *= link_score
                #print "Lex(f|e):" + str(lex_f_e)
                # Write line to file
                lex_file.write(f + " ||| " + e + " ||| " +  str(prob_f_given_e) + " " + str(prob_e_given_f) + " " + str(lex_f_e) + " " + str(lex_e_f) + " ||| " + alignments)

    
def kmo_smoothing():
    w_f_given_e, w_e_given_f = generate_word_translation_probabilities()
    print_lexical_weighting(w_f_given_e, w_e_given_f)
    
if __name__ == "__main__":
    kmo_smoothing()
