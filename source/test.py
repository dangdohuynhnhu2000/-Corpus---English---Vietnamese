from processing_English import Process_E_Sentence
from processing_Vietnamese import Process_V_Sentence
from setence_alignment import Align_Sentences
from get_dict import Get_En_Dict

v_sent = "Tom tìm ra các tài liệu liên quan đến Lang"

e_sent = "Tom found the documents linking Lang to the torture flights."
e_dict = Get_En_Dict("anhviet.txt")



# Is_Matched(v_sent, trans_sent)
print(Align_Sentences(e_dict, e_sent, v_sent))