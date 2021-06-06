import nltk
import os
import re
from collections import OrderedDict
from importlib.resources import contents
from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# nltk.download()

# nltk.download('words')
# words = set(nltk.corpus.words.words())
def read_folder(folder_path, file_id,folder_id_path):
    snow_stemmer = SnowballStemmer(language='english')
    stop_list = stopwords.words("english")
    words = set(nltk.corpus.words.words())
    i = 0
    token_list = []
    file_list = {}
    token_dict = {}
    doc_file = open('docinfo.txt', 'a')
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8', errors='ignore') as f:
            file_list[filename] = file_id[i]
            position = 1
            data = f.read()
            soup = BeautifulSoup(data, "html.parser")
            text = soup.body
            if text:
                text = text.get_text()

                regex_tokens = nltk.RegexpTokenizer(r'\w+')
                tokens = regex_tokens.tokenize(text.lower())
                file_dict = {}
                for token in tokens:
                    stem = snow_stemmer.stem(token)
                    stem.lower()
                    if stem not in stop_list and re.match("^[a-zA-Z_]*$", stem):
                        token_list.append(stem)
                        if stem not in file_dict.keys():
                            file_dict[stem] = []
                        file_dict[stem].append(position)
                    position += 1
                length_of_doc = position
                for key, value in file_dict.items():
                    if key not in token_dict.keys():
                        token_dict[key] = {}
                    f_id = file_list[filename]
                    token_dict[key][f_id] = value
            doc_file.write(str(folder_id_path)+ '/' +filename + ' , ' + str(file_id[i]) + ' , ' + str(length_of_doc) + '\n')
            if i >15:
                break
            print(i)
            i += 1

    token_dict = OrderedDict(sorted(token_dict.items()))
    return token_dict


def display_dict(dict):
    # i = 0
    for r, y in dict.items():
        print(r, y)
        # i += 1
        # if i > 100:
        #    break


def inverted_index(token_dict,path_choosen):
    terms_file = open('index_' + str(path_choosen) + '_terms.txt', 'w')
    positing_file = open('index_' + str(path_choosen) + '_postings.txt', 'w')

    # counter is document frequency
    # c is term frequency
    byte_size=0
    inverted_dict = {}
    for r, y in token_dict.items():
        counter = 0
        inverted_dict[r] = {}
        term_list=r+' '+str(byte_size)+'\n'
        posting_list= str(len(y))
        d_gap=0
        for a, b in y.items():
            n = []
            c = 0
            if counter == 0:
                d_gap=a
                inverted_dict[r][a] = n
                prev = a
            if counter != 0:
                d_gap = a - prev
                prev = a
                inverted_dict[r][d_gap] = n
            posting_list += ' ' + str(d_gap)+ ' ' + str(len(b))
            for s in b:
                if c == 0:
                    p = s
                    data=s
                    n.append(s)
                if c != 0:
                    data=s-p
                    n.append(s - p)
                c += 1
                posting_list += ' '+str(data)
            counter += 1
        posting_list += '\n'
        terms_file.write(term_list)
        positing_file.write(posting_list)
        byte_size += len(posting_list) + 1

    terms_file.close()
    positing_file.close()


def main():
    ID1 = [x for x in range(1, 1162)]
    ID2 = [x for x in range(1162, 1162 + 1105)]
    ID3 = [x for x in range(1162 + 1105, 1162 + 1105 + 1229)]
    done=0
    path1 = r"C:/Users/DELL/PycharmProjects/pythonProject1/corpus1/1"
    path2 = r"C:/Users/DELL/PycharmProjects/pythonProject1/corpus1/2"
    path3 = r"C:/Users/DELL/PycharmProjects/pythonProject1/corpus1/3"
    while True:
        path_choosen = int(input("Enter 1, 2, 3 to select folder:"))
        if path_choosen == 1:
            path = path1
            ID = ID1
        elif path_choosen == 2:
            path = path2
            ID = ID2
        elif path_choosen == 3:
            path = path3
            ID = ID3
        dic1 = read_folder(path, ID,path_choosen)
        inverted_index(dic1,path_choosen)
        done += 1
  #      display_dict(dic1)
        if done == 3:
            break






main()
