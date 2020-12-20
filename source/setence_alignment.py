from get_dict import Get_En_Dict
from processing_Vietnamese import Max_Matched, Process_V_Sentence
from processing_English import Process_E_Sentence
SENT_RATIO = 0.5
LEN_SENT_RATIO = 0.7



def Align_Sentences(e_dict, e_sent, v_sent):
    new_e_sent = Process_E_Sentence(e_sent)
    new_v_sent = Process_V_Sentence(v_sent)
    if Len_Sent_Ratio(new_e_sent, new_v_sent):
        if Has_Matched_Sentences(e_dict, new_e_sent, new_v_sent):
            print('e_sent: ', new_e_sent)
            print('v_sent: ', new_v_sent)
            return True
    return False


def Has_Matched_Sentences(e_dict, e_sent, v_sent):
    #duyet tung tu trong cau
    trans_words = [] 
    for i in range(len(e_sent)):
        e_word = e_sent[i]
        if e_word in e_dict.keys():
            #print('e_w: ', e_word)
            v_words = e_dict[e_word]
            max_matched_w = ''
            max_matched_w = Max_Matched(v_words, v_sent)
            #print('max matched: ', max_matched_w)
            if max_matched_w != '':
                trans_words.append(max_matched_w)
        else:
            trans_words.append(e_word)
    
    trans_sent = List_To_String(trans_words)
    v_sent = List_To_String(v_sent)
    print('trans_sent: ', trans_sent)
    print('v_sent: ', v_sent)
    if Is_Matched(v_sent, trans_sent):
        return True
    return False



def Get_Possible_Sentences(total_list):
    list_sents = []
    for x in range(len(total_list[0])):
        list_sents.append([total_list[0][x]])
    for i in range(1, len(total_list)):
        old_list = list(list_sents)
        list_sents = []
        for k in range(len(old_list)):
            new_list = []
            for j in range(len(total_list[i])):
                new_list.append(old_list[k] + [total_list[i][j]])
            list_sents.extend(new_list)
    #print('list sent: ', list_sents)
    return list_sents

#Input: vi_sent: cau tieng viet, e_sent: cau tieng Anh tuong ung
#Output: tra ve True neu cau co ti le duoc chap nhan, nguoc lai tra ve false
def Is_Matched(vi_sent, trans_sent):
    vi_sent = vi_sent.split()
    len1 = len(vi_sent)
    trans_sent = trans_sent.split()
    len2 = len(trans_sent)
    intersect = 0
    inter = []


    #tim so hinh vi giao
    for w in vi_sent:
        # print('w: ', w)
        if w in trans_sent:
            intersect += 1
            trans_sent.remove(w)
            inter.append(w)
    ratio = 2 * intersect / (len1 + len2)
    
    if ratio > 0 and len(inter) > 0:
        print('intersect: ', inter)
        print('ratio: ', ratio)

    if ratio >= SENT_RATIO:
        return True
    return False
    

def List_To_String(sent):
    return ' '.join(sent)


def Get_Max_Len_Stopwords(list_stopwords):
    max_len = 0
    for e in list_stopwords:
        if len(e.split()) > max_len:
            max_len = len(e.split())
    return max_len


def Len_Sent_Ratio(e_sent, v_sent):
    if (len(e_sent)) == 0 or (len(v_sent) == 0):
        return False
    if len(e_sent) > len(v_sent):
        len_ratio = len(e_sent) / len(v_sent)
    else:
        len_ratio = len(v_sent) / len(e_sent)
    
    if len_ratio > LEN_SENT_RATIO:
        return True
    return False






