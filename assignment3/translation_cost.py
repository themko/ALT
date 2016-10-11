import os.path
import cPickle as pickle
import time
 
def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def language_model_cost(phrases,lm,f_line):
    score = 0
    for phrase in phrases:    
        e= phrase[1]
        f_al_start =int(phrase[0].split('-')[0])
        f_al_stop =int(phrase[0].split('-')[1])
        #Get list of words from the f_line
        f = f_line[f_al_start:f_al_stop+1]
        f = ' '.join(f)
        f_prob = lm[f][0]
        score += (-1 * f_prob)
    return score

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

def translation_cost(p_table,lm):
    print 'start'
    #Run through all the traces and calculate the total translation cost
    with open('testresults.trans.txt.trace','r') as traces:
        with open('file.test.de') as f_file:
            for f_line,trace in zip(f_file,traces):
                trace = trace.split(' ||| ')
                f_line = f_line.split()
                phrases = [tuple(p.split(':',1)) for p in trace]
                print phrases
                translation_model_cost = translation_model_cost(phrases,p_table,f_line)
                print 'tm_cost',translation_model_cost
                language_model_cost = language_model_cost(phrases, lm, f_line)
                ###
                language_model_cost = 0
                reordering_model_cost = 0

def translation_model_cost(phrases,p_table,f_line):
    model_output = 0
    #For the phrases in the trace give the four translation model weights
    for phrase in phrases:
        e= phrase[1]
        
        f_al_start =int(phrase[0].split('-')[0])
        f_al_stop =int(phrase[0].split('-')[1])
        #Get list of words from the f_line
        f = f_line[f_al_start:f_al_stop+1]
        f = ' '.join(f)
        print f_line
        try:
            print phrase, (f,e)
            print 'ptable_phrase', p_table[(f,e)]
            p_fe,lex_fe,p_ef,lex_ef, word_pen = p_table[(f,e)]
            w_p_fe,w_lex_fe,w_p_ef,w_lex_ef,word_pen = -1,-1,-1,-1,-1
            #For now assumed to be the sum of all the probs
            phrase_cost = -1*p_fe + -1 * lex_fe + -1*p_ef + -1*lex_ef + -1*word_pen
        except KeyError:
            print 'No key for: ',(f,e)
            phrase_cost = 0
        #Assumes every phrase has equal importance. Summing over all of them
        model_output+= phrase_cost
        
    return model_output

#phrase_table = read_phrase_table('phrase-table')
#language_model =read_language_model('file.en.lm')
#phrase_table = 0
#language_model = 0
#translation_cost(phrase_table, language_model)
    

