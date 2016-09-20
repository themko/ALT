from collections import defaultdict

def transition_probabilities():
    print 'start'
    with open('phrases.txt', 'r') as phrases_file: #open the file
        phrases = phrases_file.readlines()    
    
    for line in phrases:
        f,e, probs = line.split("|||")
        prob_f, prob_e, prob_f_e = probs.split()
        print f
        print e
        print prob_f
        print prob_e
        print prob_f_e

transition_probabilities()
