from pyvi import ViTokenizer, ViPosTagger
import re


def Get_List_V_Sent(paragraph):
    list_sents = []
    words_in_sent = []
    list_tagged_word = ViPosTagger.postagging(ViTokenizer.tokenize(paragraph))
    list_word = list_tagged_word[0] #lay ra cac tu
    list_pos = list_tagged_word[1] #lay ra cac nhan tuong ung voi cac tu
    for i in range(len(list_word)):
        #them tu vao cau
        if list_pos[i] != 'F':
            list_word[i] = list_word[i].replace('_', ' ')
            words_in_sent.append(list_word[i])
        if (list_pos[i] == 'F') and (list_word[i] in '.!?'): #neu gap dau ket thuc cau 
            sentence = ' '.join(words_in_sent)
            sentence += list_word[i] #them dau ket thuc cau
            list_sents.append(sentence)
            words_in_sent = []

    return list_sents



def Process_V_Sentence(sent):
    #tach tu va lay nhan cho tu
    processed_sent = []
    list_tagged_word = ViPosTagger.postagging(ViTokenizer.tokenize(sent))
    list_word = list_tagged_word[0] #lay ra cac tu
    list_pos = list_tagged_word[1] #lay ra cac nhan tuong ung voi cac tu
    for i in range(len(list_word)):
        #them tu vao cau
        if list_pos[i] not in ['F', 'P']:
            if list_pos[i] not in ['Ny', 'Np']:
                list_word[i] = list_word[i].lower()
            list_word[i] = list_word[i].replace('_', ' ')
            processed_sent.append(list_word[i])

    #loai bo cac stop word trong cau
    processed_sent = Eliminate_V_Stop_Word("v_stopwords.txt", processed_sent)

    return processed_sent


def Get_V_Stopwords(filename):
    f = open(filename, "r", encoding='utf8')
    lines = f.readlines()
    f.close()

    v_stopwords = []
    for line in lines:
        if line[-1] == '\n':
            line = line[:-1] #bo dau \n cuoi dong
        v_stopwords.append(line)
    return v_stopwords




def Eliminate_V_Stop_Word(filename, sent):
    v_stopwords = Get_V_Stopwords(filename)
    new_sent = []
    for w in sent:
        if w not in v_stopwords:
            new_sent.append(w)
    return new_sent


def Same_Morpho_Ratio(word1, word2):
    li_mor1 = word1.split()
    len1 = len(li_mor1)
    li_mor2 = word2.split()
    len2 = len(li_mor2)
    intersect = 0
    for mor in li_mor1:
        if mor in li_mor2:
            intersect += 1
            li_mor2.remove(mor)
    
    ratio = 2*intersect/(len1 + len2)
    return ratio


def Has_Intersect_Morpho(trans_word, v_sent):
    for i in range(len(v_sent)):
        if Same_Morpho_Ratio(v_sent[i], trans_word) >= 0.5:
            return True
    return False

def Max_Matched(list_trans_word, v_sent):
    max_ratio = 0
    max_matched_w = ''
    for trans_w in list_trans_word:
        for v_word in v_sent:
            if Same_Morpho_Ratio(trans_w, v_word) > max_ratio:
                max_ratio = Same_Morpho_Ratio(trans_w, v_word)
                max_matched_w = trans_w
    return max_matched_w
