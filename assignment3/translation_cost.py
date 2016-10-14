import os.path
import cPickle as pickle
import time
import math
 
def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def read_phrase_table(file_name):
    print 'reading phrase table'
    phrases = {}
    if(os.path.isfile('pt.p')):
        print '    now reading in pickle'
        with open('pt.p', 'rb') as pt_pickle:
            phrases = pickle.load(pt_pickle)
    else:
        with open(file_name, 'r') as table:
            for line in table:
                line = line.split(' ||| ')
                f = line[0]
                e = line[1]
                probs = [float(p) for p in line[2].split()]
                #leaving alignments out
                phrases[(f,e)] = probs
        with open('pt.p','wb') as pt_pickle:
            print '    dumping pickle'
            pickle.dump(phrases,pt_pickle)    
    return phrases

def read_language_model(file_name):
    print 'reading language model'
    lms = {}
    if(os.path.isfile('lm.p')):
        print '    now reading in pickle'
        with open('lm.p', 'rb') as lm_pickle:
            lms = pickle.load(lm_pickle)
    else:
        with open(file_name, 'r') as language_model:
            gram_counter = 0
            for line in language_model:
                if line[0] == "\\":
                    if line[-7:-1] == 'grams:':
                        #Only stable up to 9-grams
                        gram_counter= int(line[1])
                    continue
                #Avoid reading in lines in file before gram counts
                line = line.split()
                if gram_counter!=0 and len(line)>0:
                    prob = float(line[0])
                    if is_float(line[-1]):
                        backoff_prob = float(line[-1])
                        words = line[1:-1]
                    else:
                        backoff_prob = 0
                        words = line[1:]
                    #Pass phrase as key for probabilities
                    f = ' '.join(words)
                    lms[f] = (prob,backoff_prob)
        with open('lm.p','wb') as lm_pickle:
            print '    dumping pickle'
            pickle.dump(lms,lm_pickle)
    return lms

def read_reordering_file(file_name):
    print 'reading reordering file'
    reorderings = {}
    if(os.path.isfile('reorder.p')):
        print '    now reading in pickle'
        with open('reorder.p', 'rb') as reorder_pickle:
            reorderings = pickle.load(reorder_pickle)
    else:
        ##
        with open(file_name, 'r') as reorder_file:
            for line in reorder_file:
                line = line.split(' ||| ')
                f = line[0]
                e = line[1]
                probs = [float(p) for p in line[2].split()]
                #leaving alignments out
                reorderings[(f,e)] = probs
                
        with open('reorder.p','wb') as reorder_pickle:
            print '    dumping pickle'
            pickle.dump(reorderings,reorder_pickle)    
    return reorderings
    
 
def language_model_cost(phrase,lm):
    cost = 0
    e= phrase
    words = e.split()
    # For all words w_n in phrase
    for cur_pos in range(0,len(words)):
        # History: w1,...w_{n-1}
        history_pos = range(0,cur_pos)
        history = [words[pos] for pos in history_pos]
        
        w_n = words[cur_pos]
        
        # Do not take into account unigram of first word, if first word is <s>
        if cur_pos == 0 and w_n == "<s>":
            continue
        
        print "w_n: ", str(w_n) + ", history: " + str(history)
        # Language model of a phrase is sum of p(w_n| w1,...,w_{n-1}) for every w_n
        cost_word = word_cost(w_n,history, lm)
        cost += cost_word
        print "total cost: " + str(cost_word)
    cost *= -1
    return cost

# Recursive method for backoff
def word_cost(w_n,history, lm, backoff=False):
    print "    w_n: ", str(w_n) + ", history: " + str(history)
    cost = 0
    n_gram = ' '.join(history + [w_n])
    print "    n_gram: " + n_gram
    if n_gram in lm:
        print "    normal cost: " + str(lm[n_gram][0])
        cost = lm[n_gram][0]
        if backoff:
            print "    backoff cost: " + str(lm[n_gram][1])
            cost += lm[n_gram][1]
    else:
        # n-gram not available
        if len(history) > 0:
            #backoff to shorter history w_2...w_{n-1}
            print "backoff"
            new_history = history[1:]
            # Recursive call of word_cost, and add backoff probability
            cost = word_cost(w_n,new_history, lm, backoff=True)
        else:
            # Assign cost=0 if unigram is not available
            cost = 0
    return cost



def reorder_model_cost(phrase,trace,reorder_file,f_line):
    #Get the index of the phrase in the trace sentence
    phr_ind = ''.join([str(phrase[0]),':',str(phrase[1])])
    
    phr_position =  trace.index(phr_ind)
    prev_phrase_align = trace[phr_position - 1].split(':')[0]
    if (phr_position != len(trace)-1):
        next_phrase_align = trace[phr_position + 1].split(':')[0]
    else:
        next_phrase_align = 'end-end'
    next_phrase_align_begin, next_phrase_align_end = next_phrase_align.split('-')
    prev_phrase_align_begin, prev_phrase_align_end = prev_phrase_align.split('-')

    model_output= 0
    e= phrase[1].rstrip()
    f_al_begin =int(phrase[0].split('-')[0])
    f_al_end =int(phrase[0].split('-')[1])

    #Get list of words from the f_line
    f = f_line[f_al_begin:f_al_end+1]
    f = ' '.join(f).rstrip()
    try:
        probs = reorder_file[(f,e)]
        rl_m,rl_s,rl_d,lr_m,lr_s,lr_d = probs
        RL_cost = 0
        LR_cost = 0
        #Check if phrase is first in sentence
        if phr_position == 0:
            RL_cost = rl_m
        else:
            if (int(prev_phrase_align_end) == f_al_begin -1):
                RL_cost = rl_m
            elif (int(prev_phrase_align_begin) == f_al_end + 1):
                RL_cost = rl_s
            else:
                RL_cost = rl_d
        #Check if phrase is last in sentence
        if phr_position == len(trace) -1 :
            LR_cost = lr_m
        else:
            if int(next_phrase_align_begin) == f_al_end +1:
                LR_cost = lr_m
            elif int(next_phrase_align_end) == f_al_begin -1:
                LR_cost = lr_s
            else:
                LR_cost = lr_d
        #Assumed that probabilities of both directions are multiplied with eachother
        phrase_cost = LR_cost * RL_cost
        #Take log-probability
        phrase_cost = math.log10(phrase_cost)
        phrase_cost *= -1
    except KeyError:
        phrase_cost = 0
    model_output += phrase_cost
    return model_output

def translation_model_cost(phrase,p_table,f_line):
    #For the phrases in the trace give the four translation model weights
    e= phrase[1].rstrip()
    
    f_al_start =int(phrase[0].split('-')[0])
    f_al_stop =int(phrase[0].split('-')[1])
    #Get list of words from the f_line
    f = f_line[f_al_start:f_al_stop+1]
    f = ' '.join(f).rstrip()
    #print f_line
    try:
        #print (f,e)
        #print 'ptable_phrase', p_table[(f,e)]
        p_fe,lex_fe,p_ef,lex_ef, word_pen = p_table[(f,e)]
        #For now assumed to be the sum of all the probs (weighted by 1)
        phrase_cost = 1*math.log10(p_fe) + 1 * math.log10(lex_fe) + 1*math.log10(p_ef) + 1*math.log10(lex_ef) + 1*word_pen
        phrase_cost = -1*phrase_cost
    except KeyError:
        #print 'KeyError',(f,e)
        if f!= e:
            print 'ERROR! No key for: ',(f,e)
        ##IS this a good cost for a non-translated phrase?
        phrase_cost = 0
    #Assumes every phrase has equal importance. Summing over all of them
    return phrase_cost
    

def translation_cost(p_table,lm,reorder_file):
    print 'start'
    #Run through all the traces and calculate the total translation cost
    with open('testresults.trans.txt.trace','r') as traces:
        with open('file.test.de', 'r') as f_file:
            with open('cost_output.txt','w') as output_file:
                sentence_cost_list = []
                for f_line,trace in zip(f_file,traces):
                    trace = trace.split(' ||| ')
                    f_line = f_line.split()
                    phrases = [tuple(p.split(':',1)) for p in trace]
                    #print phrases
                    cost_per_phrase = []
                    for i in range(0,len(phrases)):
                        phrase = phrases[i]
                        print phrase
                        phrase_reordering_model_cost = 0 # reorder_model_cost(phrase,reorder_file,f_line)
                        phrase_translation_model_cost = 0 # translation_model_cost(phrase,p_table,f_line)
                        if phrase_translation_model_cost >0:
                            print 'ERROR! tm_cost',phrase_translation_model_cost, 'from', phrase
                            ###
                        # For the language model, start and end symbols have to be added to the phrase
                        # Positions in the foreign phrase are discarded.
                        phrase_lm = phrase[1]
                        if i==0:
                            phrase_lm = "<s> " + phrase[1]
                        if i ==len(phrases):
                            phrase_lm = phrase[1] + " </s>"
                        phrase_language_model_cost = language_model_cost(phrase_lm, lm)
                        print "Language model: " + str(phrase_language_model_cost)
                        print "Translation model: " + str(phrase_translation_model_cost)
                        print "Reordering model: " + str(phrase_reordering_model_cost)
                        phrase_penalty = 1
                        phrase_cost = 1 * phrase_reordering_model_cost + 1 * phrase_translation_model_cost + 1 * phrase_language_model_cost + 1 * phrase_penalty
                        print "Phrase cost: " + str(phrase_cost)
                        cost_per_phrase.append(phrase_cost)
                    sentence_cost = sum(cost_per_phrase)
                    output_file.write(str(sentence_cost)+"\n")
    
reorder_file = 0#read_reordering_file('dm_fe_0.75')
phrase_table = 0#read_phrase_table('phrase-table')
language_model =read_language_model('file.en.lm')

translation_cost(phrase_table, language_model,reorder_file)

