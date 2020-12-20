from setence_alignment import Align_Sentences
from get_dict import Get_En_Dict
from processing_English import Get_List_E_Sent
from processing_Vietnamese import Get_List_V_Sent

SENT_DISTANCE = 5 #so sanh 1 cau voi 5 cau tuong ung trong doan dich song ngu

def Process_Data_Source_1(filename, output_file):
    f = open(filename, "r", encoding="utf8")
    lines = f.readlines()
    f.close()
    e_sent = ''
    v_sent = ''
    e_dict = Get_En_Dict("anhviet.txt")
    ID = 0

    file_out = open(output_file, "w", encoding="utf8")
    
    #kiem tra da xuat hien 2 cau song ngu tuong ung chua
    exist_e = False
    exist_v = False

    for line in lines:
        if not line:
            continue
        #loai bo dau '\n' cuoi moi dong
        if line[-1] == '\n':
            line = line[:-1]

            l_square = line.find('[')
            r_square = line.find(']')

            sent_id = line[l_square + 1 : r_square]
            sent_id = sent_id.split('_')
            lang = sent_id[1]

            if lang == 'v':
                v_sent = line[r_square + 2 :]
                exist_v = True
            else:
                e_sent = line[r_square + 2 :]
                exist_e = True

            #neu da ton tai du cap cau song ngu thi tien hanh giong hang cau va in vao file
            if exist_e and exist_v:
                if Align_Sentences(e_dict, e_sent, v_sent):
                    ID += 1
                    e_sent_id = '[' + str(ID) + '_' + 'e' + ']'
                    file_out.write(e_sent_id + ' ' + e_sent + '\n')
                    v_sent_id = '[' + str(ID) + '_' + 'v' + ']'
                    file_out.write(v_sent_id + ' ' + v_sent + '\n')
                exist_e = False
                exist_v = False
    file_out.close()


def Process_Data_Source_2(input_file, output_file):
    fi = open(input_file, "r", encoding="utf8")
    lines = fi.readlines()
    fi.close()
    e_dict = Get_En_Dict("anhviet.txt")
    
    list_sents = []

    for line in lines:
        line = line.replace('\n', '')
        line = line.replace('\xa0', '')
        line = line.replace('\u200b', '')
        if line != '':
            list_sents.append(line)
    
    #chia thanh cac doan
    e_list = dict()
    v_list = dict()
    for sent in list_sents:
        if sent.find('[') != -1:
            para_id = sent[1:-1]
            para_id = para_id.split('_')
            lang = para_id[1]
            num = para_id[0]
            paragraph = []
        else:
            if lang == 'e':
                li_sents = Get_List_E_Sent(sent)
            else:
                li_sents = Get_List_V_Sent(sent)
            paragraph.extend(li_sents)
            if lang == 'e':
                e_list[num] = paragraph
            else:
                v_list[num] = paragraph
    
    out_file = open(output_file, "w", encoding="utf8")

    ID = 0
    #tien hanh giong hang cau
    for para_id_num in e_list.keys():
        #danh dau cac vi tri da duoc giong hang
        v_selected = []
        for i in range(len(e_list[para_id_num])):
            e_sent = e_list[para_id_num][i]
            #so sanh voi 5 cau co vi tri tuong ung gan no
            for j in range(-2, 3):
                x = i + j
                if (x >= 0) and (x < len(v_list[para_id_num])) and (x not in v_selected):
                    v_sent = v_list[para_id_num][x]
                    if Align_Sentences(e_dict, e_sent, v_sent):
                        #in vao file
                        ID += 1
                        sent_id = '[' + str(ID) + '_' + 'e' + ']'
                        out_file.write(sent_id + ' ' + e_sent + '\n')
                        sent_id = '[' + str(ID) + '_' + 'v' + ']'
                        out_file.write(sent_id + ' ' + v_sent + '\n')
                        #danh dau vi tri cua cau tieng Viet da duoc giong hang
                        v_selected.append(x)
                        break

    out_file.close()

        


Process_Data_Source_2("unicef.txt", "corpus_unicef.txt")