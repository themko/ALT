import os.path
import cPickle as pickle
import time
 
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
                        words = line[1:-2]
                    else:
                        backoff_prob = 0
                        words = line[1:-1]
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
    
 
def language_model_cost(phrase,lm,f_line):
    score = 0
    e= phrase[1]
    f_al_start =int(phrase[0].split('-')[0])
    f_al_stop =int(phrase[0].split('-')[1])
    #Get list of words from the f_line
    f = f_line[f_al_start:f_al_stop+1]
    f = ' '.join(f)
    f_prob = lm[f][0]
    # Calculate score by summing over log probabilities of words
    score += (f_prob)
    return score


def reorder_model_cost(phrase,reorder_file,f_line):
    model_output= 0
    e= phrase[1].rstrip()
    f_al_start =int(phrase[0].split('-')[0])
    f_al_stop =int(phrase[0].split('-')[1])
    #Get list of words from the f_line
    f = f_line[f_al_start:f_al_stop+1]
    f = ' '.join(f).rstrip()
    try:
        probs = reorder_file[(f,e)]
        rl_m,rl_s,rl_d,lr_m,lr_s,lr_d = probs
        ##MOST LIKELY INCORRECT USE OF PROBS:
        phrase_cost= (rl_m+rl_s+rl_d+lr_m+lr_s+lr_d)
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
        phrase_cost = 1*p_fe + 1 * lex_fe + 1*p_ef + 1*lex_ef + 1*word_pen
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
        with open('file.test.de') as f_file:
            sentence_cost_list = []
            for f_line,trace in zip(f_file,traces):
                trace = trace.split(' ||| ')
                f_line = f_line.split()
                phrases = [tuple(p.split(':',1)) for p in trace]
                #print phrases
                cost_per_phrase = []
                for phrase in phrases:
                    phrase_reordering_model_cost = reorder_model_cost(phrase,reorder_file,f_line)
                    phrase_translation_model_cost = translation_model_cost(phrase,p_table,f_line)
                    if phrase_translation_model_cost >0:
                        print 'ERROR! tm_cost',phrase_translation_model_cost, 'from', phrase
                        ###
                    phrase_language_model_cost = 0
                    phrase_cost = 1 * phrase_reordering_model_cost + 1 * phrase_translation_model_cost + 1 * phrase_language_model_cost
                    cost_per_phrase.append(phrase_cost)
                sentence_cost = sum(cost_per_phrase)
                sentence_cost_list.append(sentence_cost)
    

reorder_file = read_reordering_file('dm_fe_0.75')
phrase_table = read_phrase_table('phrase-table')
language_model =read_language_model('file.en.lm')
#phrase_table = 0
#language_model = 0
translation_cost(phrase_table, language_model,reorder_file)
    

