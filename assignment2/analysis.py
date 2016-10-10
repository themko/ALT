from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt



def perform_analysis(filename,title):
    with open(filename,"r") as phrases_file_phrasebased:
        # Sum reordering probabilities from all phrases
        reorderings_dict = defaultdict(float)
        for line in phrases_file_phrasebased:
            f,e, probs = line.split("|||")
            p_m_LR, p_s_LR, p_d_left_LR, p_d_right_LR, p_m_RL, p_s_RL, p_d_left_RL, p_d_right_RL, = probs.split()
            reorderings_dict["m_LR"] += float(p_m_LR)
            reorderings_dict["s_LR"] += float(p_s_LR)
            reorderings_dict["d_l_LR"] += float(p_d_left_LR)
            reorderings_dict["d_r_LR"] += float(p_d_right_LR)
            
            reorderings_dict["m_RL"] += float(p_m_RL)
            reorderings_dict["s_RL"] += float(p_s_RL)
            reorderings_dict["d_l_RL"] += float(p_d_left_RL)
            reorderings_dict["d_r_RL"] += float(p_d_right_RL)
        print title + ":"
        print reorderings_dict
        reorderings = reorderings_dict.keys()
        summed_probs = reorderings_dict.values()
        x_axis = range(0,len(reorderings)) # 8 reorderings
        plt.xticks(x_axis,reorderings)
        plt.bar(x_axis,summed_probs)
        plt.title(title)
        plt.show()
        
def perform_len_analysis(filename,title,length,lang):
    with open(filename,"r") as phrases_file_phrasebased:
        # Sum reordering probabilities for all phrases with a certain length
        reorderings_dict = defaultdict(float)
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
                reorderings_dict["m_LR"] += float(p_m_LR)
                reorderings_dict["s_LR"] += float(p_s_LR)
                reorderings_dict["d_l_LR"] += float(p_d_left_LR)
                reorderings_dict["d_r_LR"] += float(p_d_right_LR)
                
                reorderings_dict["m_RL"] += float(p_m_RL)
                reorderings_dict["s_RL"] += float(p_s_RL)
                reorderings_dict["d_l_RL"] += float(p_d_left_RL)
                reorderings_dict["d_r_RL"] += float(p_d_right_RL)
        print title + ":"
        print reorderings_dict
        
        reorderings = reorderings_dict.keys()
        summed_probs = reorderings_dict.values()
        x_axis = range(0,len(reorderings)) # 8 reorderings
        plt.xticks(x_axis,reorderings)
        plt.bar(x_axis,summed_probs)
        plt.title('Phrase length:'+str(length)+' '+title)
        plt.savefig(title+ lang_title+' lenght='+str(i))
        plt.close()
            
if __name__ == "__main__":
    perform_analysis("reorder_est_phrasebased.txt","Summed phrased-based reordering probabilities")
    perform_analysis("reorder_est_wordbased.txt","Summed word-based reordering probabilities")
    for i in range(1,8):
        print i
        perform_len_analysis("reorder_est_phrasebased.txt","Phrased-based reordering probabilities",i,'F')
        perform_len_analysis("reorder_est_wordbased.txt","Word-based reordering probabilities",i,'F')
        perform_len_analysis("reorder_est_phrasebased.txt","Phrased-based reordering probabilities",i,'E')
        perform_len_analysis("reorder_est_wordbased.txt","Word-based reordering probabilities",i,'E')
