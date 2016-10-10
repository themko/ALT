import os.path
import cPickle as pickle
def translation_cost():
    print 'start'
    #Run through all the traces and calculate the total translation cost
    with open('testresults.trans.txt.trace','r') as traces:
        for trace in traces:
            trace = trace.split(' ||| ')
            phrases = [tuple(p.split(':',1)) for p in trace]
            translation_model_cost = trans_model(phrases,phrase_table,)
            ###
            
def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
def trans_model(phrases):
    model_output = []
    for phrase in phrases:
        a = 0
    return model_output

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

phrase_table = read_phrase_table('phrase-table')
#language_model =read_language_model('file.en.lm')

#translation_cost()
    

