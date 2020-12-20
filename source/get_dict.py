import re

#Input: file tu dien Anh-Viet
#Output: file tu dien Anh-Viet sau khi da xu ly va duoc luu co cau truc
def Get_En_Dict(filename):
    file = open(filename, "r", encoding = "utf8")
    lines = file.readlines()
    file.close()
    e_dict = dict()
    e_word = ''
    exclamtion = False #cho biet truoc do co xuat hien dau cham than hay khong
    list_reprocess = [] #cac tu ma co nghia tuong tu mot tu khac trong tu dien


    for line in lines:

        line = line[:-1]

        if not line:
            continue

        if line[0] == '@':

            if line.find('/') != -1 : 
                e_word = line[:line.find('/')] #tu tieng Anh dung truoc cap dau phien am / /
            else: 
                e_word = line

            e_word = e_word.lower()
            e_word = e_word[1:] #bo phan tu @ o dau tu

            #loai bo cac tu trong cap dau ngoac ()
            if e_word.find('(') != -1:
                w = ''
                parentheses = 0
                for c in e_word:
                    if c == '(':
                        parentheses += 1
                    elif c == ')':
                        parentheses -= 1
                    else:
                        if parentheses == 0:
                            w += c 
                
                e_word = w

            e_word = ' '.join(e_word.split()) #loai bo cac khoang trong khong can thiet
            #neu key e_word chua ton tai truoc do thi khoi tao list nghia trong cho e_word
            if e_word not in e_dict.keys():
                e_dict[e_word] = list()
            
        
        if line[0] == '!':
            exclamtion = True
        
        if (line[0] != '!') and (line[0] != '-'):
            exclamtion = False

        
        #nhung dong bat dau bang '-' theo sau 1 dong bat dau bang '!' thi khong phai la nghia cua tu tieng anh
        if (line[0] == '-') and (exclamtion == False):
            line = line[2:] #loai bo '- ' dau dong
           
            #loai bo cac tu trong cap dau ngoac trong dong
            new_line = ''
            if line.find('(') != -1:
                parentheses = 0
                for c in line:
                    if c == '(':
                        parentheses += 1
                    elif c == ')':
                        parentheses -= 1
                    else:
                        if parentheses == 0:
                            new_line += c 
                line = new_line

            #tach cac tu dua vao cac dau
            v_words = re.split('[,;./]', line)
           
            for i in range(len(v_words)):
                if not v_words[i]:
                    continue

                new_word = v_words[i]


               #loai bo cac khoang trang khong can thiet
                new_word = ' '.join(new_word.split())

                if new_word and e_word:
                    v_words[i] = new_word

                    new_words = new_word.split()
                    if len(new_words) > 1:
                        if new_words[0] == 'xem': 
                            same_word = new_word[4:] #lay tu tieng anh sau chu 'xem '
                            list_reprocess.append([e_word, same_word])

                    #truong hop tu tieng Anh dong nghia theo sau dau =
                    if '=' in new_word:
                        li = new_word.split('=')
                        li[0] = ' '.join(li[0].split())
                        li[1] = ' '.join(li[1].split())
                        #them tu moi vao tu dien
                        if li[1] in e_dict.keys():
                            e_dict[li[1]].append(li[0])
                            
                        else: 
                            e_dict[li[1]] = [li[0]]

                        v_words[i] = li[0]
                    e_dict[e_word].append(v_words[i])

    
    #xu ly nhung tu co nghia duoc bieu dien boi 1 tu tieng Anh khac trong tu dien
    for w in list_reprocess:
        if w[1] in e_dict.keys():
            e_dict[w[0]] = e_dict[w[1]]
    

    return e_dict




        
        

    