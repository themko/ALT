from collections import defaultdict

def transition_probabilities():
    print 'start'
    with open('phrases.txt', 'r') as phrases_file: #open the file
        phrases = phrases_file.readlines()    
    
    with open("transition_probs.txt","w") as probs_file:
        for line in phrases:
            f,e, probs = line.split("|||")
            prob_f, prob_e, prob_f_e = probs.split()
            # P(F|E) = P(F,E) / P(E)
            prob_f_given_e = float(prob_f_e) / float(prob_e)
            
            # P(E|F) = P(F,E) / P(F)
            prob_e_given_f = float(prob_f_e) / float(prob_f)
            
            # Write line to file
            probs_file.write(f + " ||| " + e + " ||| " +  str(prob_f_given_e) + " " + str(prob_e_given_f) + "\n")

transition_probabilities()
