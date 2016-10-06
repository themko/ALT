from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

WORD_BASED_ON = True

ORIENTATION_LR = 0
ORIENTATION_RL = 1

#orientations = ["p_m_LR", "p_s_LR", "p_d_left_LR", "p_d_right_LR", "p_m_RL", "p_s_RL", "p_d_left_RL", "p_d_right_RL"]

def perform_analysis(filename,title):
    with open(filename,"r") as phrases_file_phrasebased:
        orientations_dict = defaultdict(float)
        for line in phrases_file_phrasebased:
            f,e, probs = line.split("|||")
            p_m_LR, p_s_LR, p_d_left_LR, p_d_right_LR, p_m_RL, p_s_RL, p_d_left_RL, p_d_right_RL, = probs.split()
            orientations_dict["m_LR"] += float(p_m_LR)
            orientations_dict["s_LR"] += float(p_s_LR)
            orientations_dict["d_l_LR"] += float(p_d_left_LR)
            orientations_dict["d_r_LR"] += float(p_d_right_LR)
            
            orientations_dict["m_RL"] += float(p_m_RL)
            orientations_dict["s_RL"] += float(p_s_RL)
            orientations_dict["d_l_RL"] += float(p_d_left_RL)
            orientations_dict["d_r_RL"] += float(p_d_right_RL)
        print title + ":"
        print orientations_dict
        orientations = orientations_dict.keys()
        summed_probs = orientations_dict.values()
        x_axis = range(0,len(orientations)) # 8 orientations
        plt.xticks(x_axis,orientations)
        plt.bar(x_axis,summed_probs)
        plt.title(title)
        plt.show()
        
def perform_len_analysis(filename,title,length,lang):
    with open(filename,"r") as phrases_file_phrasebased:
           
            orientations_dict = defaultdict(float)
            for line in phrases_file_phrasebased:
                f,e, probs = line.split("|||")
                lang_line = ''
                lang_title = ''
                if(lang==('E')):
                    lang_line =e.split()
                    lang_title = 'E'
                elif(lang==('F')):
                    lang_line=f.split()
                    lang_title = 'F'
                else:
                    print 'error'
                    break
                if len(lang_line) ==length:
                    p_m_LR, p_s_LR, p_d_left_LR, p_d_right_LR, p_m_RL, p_s_RL, p_d_left_RL, p_d_right_RL, = probs.split()
                    orientations_dict["m_LR"] += float(p_m_LR)
                    orientations_dict["s_LR"] += float(p_s_LR)
                    orientations_dict["d_l_LR"] += float(p_d_left_LR)
                    orientations_dict["d_r_LR"] += float(p_d_right_LR)
                    
                    orientations_dict["m_RL"] += float(p_m_RL)
                    orientations_dict["s_RL"] += float(p_s_RL)
                    orientations_dict["d_l_RL"] += float(p_d_left_RL)
                    orientations_dict["d_r_RL"] += float(p_d_right_RL)
            print title + ":"
            print orientations_dict
            
            orientations = orientations_dict.keys()
            summed_probs = orientations_dict.values()
            x_axis = range(0,len(orientations)) # 8 orientations
            plt.xticks(x_axis,orientations)
            plt.bar(x_axis,summed_probs)
            plt.title('Phrase length:'+str(length)+' '+title)
            #plt.show() 
            plt.savefig(title+ lang_title+' lenght='+str(i))
            plt.close()
perform_analysis("reorder_est_phrasebased.txt","Summed phrased-based reordering probabilities")
perform_analysis("reorder_est_wordbased.txt","Summed word-based reordering probabilities")
for i in range(1,8):
    print i
    perform_len_analysis("reorder_est_phrasebased.txt","Phrased-based reordering probabilities",i,'F')
    perform_len_analysis("reorder_est_wordbased.txt","Word-based reordering probabilities",i,'F')
    perform_len_analysis("reorder_est_phrasebased.txt","Phrased-based reordering probabilities",i,'E')
    perform_len_analysis("reorder_est_wordbased.txt","Word-based reordering probabilities",i,'E')