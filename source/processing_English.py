import spacy

nlp = spacy.load("en_core_web_sm")


# def Get_E_Processed_Para_List(paragraph):
#     processed_para = []
#     sentence = []
#     list_word = []
#     list_pos = []
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(paragraph)
#     for token in doc:
#         list_word.append(token.text)
#         list_pos.append(token.pos_)
#         if token.text in '.!?':
#             sentence = [list_word, list_pos]
#             processed_para.append(sentence)
#             list_word = []
#             list_pos = []
#             sentence =[]
#     return processed_para

def Get_List_E_Sent(paragraph):
    list_sent = []
    doc = nlp(paragraph)
    for sent in doc.sents:
        list_sent.append(str(sent))
    return list_sent


def Get_E_Stopwords(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    e_stopwords = []
    for line in lines:
        if line[-1] == '\n':
            line = line[:-1] #bo dau \n cuoi dong
        e_stopwords.append(line)
    return e_stopwords



def Process_E_Sentence(sent):
    e_stopwords = Get_E_Stopwords("e_stopwords.txt")
    processed_sent = []
    doc = nlp(sent)
    for token in doc:
        if token.pos_ != 'PUNCT':
            if token.pos_ != 'PROPN':
                if token.is_stop == False:
                    w = token.lemma_
                    w = w.lower()
                    processed_sent.append(w)
            #neu la ten rieng bat dau bang chu cai viet hoa
            else:
                
                w = token.lemma_
                list_pronoun = 'i you we they it he she me mine us them him her'.split()
                if w not in list_pronoun:
                    if w not in e_stopwords:
                        processed_sent.append(w)
    return processed_sent
             









