import pymorphy3
import re
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from razdel import sentenize


import time

russian_stopwords = stopwords.words("russian")
significant_parts = ("VERB", "INFN", "PRTF", "PRTS", "GRND", "NOUN", "ADJF", "ADJS", "NUMR", "ADVB", "COMP")


class Word(object):
    def __init__(self, word, p):  # p - объект после анализа pymorphy3
        self.word = word
        list_p = set()
        k = 0
        p_len = len(p)
        while k < p_len:
            if p[k].tag.POS in significant_parts:
                list_p.add((p[k].normal_form, p[k].tag.POS))
            k += 1
        self.list_path = list_p


split_character = "[(<., «»\n\"\-!?…—+:;>)]"

unit_parts = {
    'VERB': 'Глагол',
    'NOUN': 'Существительное',
    'ADJF': 'Прилагательное',
    'NPRO': 'Местоимение',
    'CONJ': 'Союз',
    'PRCL': 'Частица',
    'ADJS': 'Краткое прилагательное',
    'ADVB': 'Наречие',
    'COMP': 'Компаратив',
    'INFN': 'Глагол (инфинитив)',
    'PRTF': 'Причастие (полное)',
    'PRTS': 'Причастие (краткое)',
    'GRND': 'Деепричастие',
    'NUMR': 'Числительное',
    'PRED': 'Предикатив',
    'PREP': 'Предлог',
    'INTJ': 'Междометие'
}
morph = pymorphy3.MorphAnalyzer()

dict_name = dict()

dict_VERB = dict()  # глагол
dict_NOUN = dict()  # существительное
dict_ADJF = dict()  # прилагательное полное
dict_ADJS = dict()  # прилагательное краткое
dict_NUMR = dict()  # числительное
dict_ADVB = dict()  # наречее
dict_COMP = dict()  # компаратив

dict_PRTF = dict()  # причастие полное
dict_GRND = dict()  # деепричастие
dict_PRTS = dict()  # причастие краткое

dict_trush = dict()  # все остальное

dict_stop_word = dict()  # стоп-слова

dict_more = dict()  # несколько значений

def processing_sentence(pr):
    # pr = pr.replace("…", "")
    # pr = pr.replace("—", "")
    pr_split = re.split(split_character, pr)
    pr_split = list(filter(None, pr_split))
    i = 0
    pr_split_len = len(pr_split)
    while i < pr_split_len:
        prr = pr_split[i].replace('\xa0', ' ').replace(" ", "").replace("\t", "")
        if re.search(r'[а-яА-ЯёЁ]', prr):
            prr = re.sub(r'[^а-яА-ЯёЁ]', '', prr)
            p = morph.parse(prr)
            # print(pr_split[i])
            w = Word(prr, p)
            if p[0].normal_form in russian_stopwords:
                if p[0].normal_form in dict_stop_word:
                    dict_stop_word[p[0].normal_form] += 1
                else:
                    dict_stop_word[p[0].normal_form] = 1
            else:
                if len(w.list_path) == 1:
                    for pp in w.list_path:

                        match pp[1]:
                            case "VERB" | "INFN":
                                if pp[0] in dict_VERB:
                                    dict_VERB[pp[0]] += 1
                                else:
                                    dict_VERB[pp[0]] = 1
                            case "NOUN":
                                if pp[0] in dict_NOUN:
                                    dict_NOUN[pp[0]] += 1
                                else:
                                    dict_NOUN[pp[0]] = 1
                            case "ADJF":
                                if pp[0] in dict_ADJF:
                                    dict_ADJF[pp[0]] += 1
                                else:
                                    dict_ADJF[pp[0]] = 1
                            case "ADJS":
                                if pp[0] in dict_ADJS:
                                    dict_ADJS[pp[0]] += 1
                                else:
                                    dict_ADJS[pp[0]] = 1
                            case "NUMR":
                                if pp[0] in dict_NUMR:
                                    dict_NUMR[pp[0]] += 1
                                else:
                                    dict_NUMR[pp[0]] = 1
                            case "ADVB":
                                if pp[0] in dict_ADVB:
                                    dict_ADVB[pp[0]] += 1
                                else:
                                    dict_ADVB[pp[0]] = 1
                            case "COMP":
                                if pp[0] in dict_COMP:
                                    dict_COMP[pp[0]] += 1
                                else:
                                    dict_COMP[pp[0]] = 1
                            case "PRTF":
                                if pp[0] in dict_PRTF:
                                    dict_PRTF[pp[0]] += 1
                                else:
                                    dict_PRTF[pp[0]] = 1
                            case "GRND":
                                if pp[0] in dict_GRND:
                                    dict_GRND[pp[0]] += 1
                                else:
                                    dict_GRND[pp[0]] = 1
                            case "PRTS":
                                if pp[0] in dict_PRTS:
                                    dict_PRTS[pp[0]] += 1
                                else:
                                    dict_PRTS[pp[0]] = 1
                            case _:
                                if pp[0] in dict_trush:
                                    dict_trush[pp[0]] += 1
                                else:
                                    dict_trush[pp[0]] = 1
                else:
                    if len(w.list_path) == 0:
                        if p[0].normal_form in dict_trush:
                            dict_trush[p[0].normal_form] += 1
                        else:
                            dict_trush[p[0].normal_form] = 1
                    else:
                        if p[0].word in dict_more:
                            dict_more[p[0].word] += 1
                        else:
                            dict_more[p[0].word] = 1
        i += 1


def bigram(pr, word, fb):
    res = list()
    pr2 = pr.replace("\n", " ")
    split_character2 = "[(.,«»\"\-!?…:—;–)]+"
    w = morph.parse(word)[0].normal_form
    pr_split = re.split(split_character2, pr2)
    pr_split = list(filter(None, pr_split))
    i = 0
    pr_split_len = len(pr_split)
    while i < pr_split_len:
        if pr_split[i] != '' and pr_split[i] != ' ':
            pr_split[i].replace('\xa0', ' ')
            p_split = re.split(" ", pr_split[i])
            j = 0
            p_split_len = len(p_split)
            while j < p_split_len:
                if p_split[j] != '' and p_split[j] != ' ':
                    for value in morph.parse(p_split[j]):
                        nf = value.normal_form
                        if nf == w and p_split_len > 1:
                            if j == 0 and p_split[j+1] != ' ' and p_split[j+1] != '' and not(morph.parse(p_split[j+1])[0].normal_form in russian_stopwords) and not((p_split[j]+' '+p_split[j+1]) in res):
                                res.append(p_split[j]+' '+p_split[j+1])
                            if j == p_split_len-1 and p_split[j-1] != ' ' and p_split[j-1] != '' and not(morph.parse(p_split[j-1])[0].normal_form in russian_stopwords) and not((p_split[j-1]+' '+p_split[j]) in res):
                                res.append(p_split[j-1]+' '+p_split[j])
                            if (j > 0) and (j < p_split_len-1):
                                if p_split[j-1] != ' ' and p_split[j-1] != '' and not(morph.parse(p_split[j-1])[0].normal_form in russian_stopwords) and not((p_split[j-1]+' '+p_split[j]) in res):
                                    res.append(p_split[j-1]+' '+p_split[j])
                                if p_split[j+1] != ' ' and p_split[j+1] != '' and not(morph.parse(p_split[j+1])[0].normal_form in russian_stopwords) and not((p_split[j]+' '+p_split[j+1]) in res):
                                    res.append(p_split[j]+' '+p_split[j+1])
                j += 1
        i += 1
    fb.write("Список биграмм:\n")
    for gg in res:
        fb.write(gg)
        fb.write('\n')
    return res

def cloud_text(dict_word):
    cloud = WordCloud(scale = 4, stopwords=stopwords,background_color='#FFFFFF').generate_from_frequencies(dict_word)
    plt.imshow(cloud)
    plt.axis('off')
    #plt.show()
    cloud.to_file("static/pict/w.jpg")


start_time = time.time()
#, encoding='utf-8'
'''f = open(file_name_read, 'r')
str_file = f.read()  # читает ВЕСЬ файл
f.close()'''


'''
list_res = bigram(str_file, "толстой")
print("толстой")
fb = open(file_name_write_bigram, 'w')
fb.write("Список биграмм:\n")
for gg in list_res:
    fb.write(gg)
    fb.write('\n')
fb.close()
print("--- %s seconds ---" % (time.time() - start_time))

kk=0
for hh in dict_more.keys():
    kk += dict_more[hh]

print("Количество нераспознаных слов:", kk)
print("Количество распознаных слов:", sum(dict_VERB.values())+sum(dict_NOUN.values())+sum(dict_ADJF.values())+sum(dict_ADJS.values())+sum(dict_NUMR.values())+sum(dict_ADVB.values())+sum(dict_COMP.values())+sum(dict_PRTF.values())+sum(dict_GRND.values())+sum(dict_PRTS.values()))
'''

def func(file_name):
    dict_name.clear()
    dict_VERB.clear()
    dict_NOUN.clear()
    dict_ADJF.clear()
    dict_ADJS.clear()
    dict_NUMR.clear()
    dict_ADVB.clear()
    dict_COMP.clear()
    dict_PRTF.clear()
    dict_GRND.clear()
    dict_PRTS.clear()
    dict_trush.clear()
    dict_stop_word.clear()
    dict_more.clear()

    f3 = open(file_name, 'r', encoding='utf8')
    f1 = f3.read()
    f3.close()
    f = open("res.txt", "w+", encoding='utf-8')
    list_pr = list(sentenize(f1))
    o = 0
    list_len = len(list_pr)
    while o < list_len:
        list_pr[o].text = list_pr[o].text.replace("\n", " ")  # нужно для красивого вывода
        # print(list_pr[o].text)
        processing_sentence(list_pr[o].text)
        o += 1
    cloud_text(dict_VERB| dict_NOUN| dict_ADJF| dict_ADJS|dict_NUMR|dict_ADVB|dict_COMP|dict_PRTF|dict_GRND|dict_PRTS|dict_more)
    f.write("Словарь по частям речи:\n")
    f.write("Слово\tЧисло поторений\n")
    if len(dict_VERB)!=0:
        f.write("Глаголы:\n")
    dict_VERB2 = sorted(dict_VERB.items())
    for u2 in dict_VERB2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_NOUN)!=0:
        f.write("\n")
        f.write("Существительные:\n")
    dict_NOUN2 = sorted(dict_NOUN.items())
    for u2 in dict_NOUN2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_ADJF) != 0:
        f.write("\n")
        f.write(unit_parts["ADJF"])
        f.write(":\n")
    dict_ADJF2 = sorted(dict_ADJF.items())
    for u2 in dict_ADJF2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_ADJS)!=0:
        f.write("\n")
        f.write(unit_parts["ADJS"])
        f.write(":\n")
    dict_ADJS2 = sorted(dict_ADJS.items())
    for u2 in dict_ADJS2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_NUMR)!=0:
        f.write("\n")
        f.write(unit_parts["NUMR"])
        f.write(":\n")
    dict_NUMR2 = sorted(dict_NUMR.items())
    for u2 in dict_NUMR2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")


    if len(dict_ADVB)!=0:
        f.write("\n")
        f.write(unit_parts["ADVB"])
        f.write(":\n")
    dict_ADVB2 = sorted(dict_ADVB.items())
    for u2 in dict_ADVB2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_COMP)!=0:
        f.write("\n")
        f.write(unit_parts["COMP"])
        f.write(":\n")
    dict_COMP2 = sorted(dict_COMP.items())
    for u2 in dict_COMP2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_PRTF)!=0:
        f.write("\n")
        f.write(unit_parts["PRTF"])
        f.write(":\n")
    dict_PRTF2 = sorted(dict_PRTF.items())
    for u2 in dict_PRTF2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_GRND)!=0:
        f.write("\n")
        f.write(unit_parts["GRND"])
        f.write(":\n")
    dict_GRND2 = sorted(dict_GRND.items())
    for u2 in dict_GRND2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_PRTS)!=0:
        f.write("\n")
        f.write(unit_parts["PRTS"])
        f.write(":\n")
    dict_PRTS2 = sorted(dict_PRTS.items())
    for u2 in dict_PRTS2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    if len(dict_trush)!=0:
        f.write("\n")
        f.write("Другие")
        f.write(":\n")
    dict_trush2 = sorted(dict_trush.items())
    for u2 in dict_trush2:
        f.write(u2[0])
        f.write("\t")
        f.write(str(u2[1]))
        f.write("\n")

    dict_more_2 = sorted(dict_more.items())
    f.write("Словарь многозначных слов:\n")
    f.write("Слово\tЧисло поторений\tНачальные формы(Возможные части речи)\n")
    for u in dict_more_2:
        f.write(u[0])
        f.write("\t")
        f.write(str(u[1]))
        f.write("\t(")
        p = morph.parse(u[0])
        word2 = Word(u[0], p)
        iii = 0
        ik = len(word2.list_path)
        while iii < ik:
            if iii != 0:
                f.write(", ")
            res_list1 = [i for i in word2.list_path]
            f.write(res_list1[iii][0])
            f.write("(")
            f.write(unit_parts[res_list1[iii][1]])
            f.write(")")
            iii += 1
        f.write(")\n")
    f.close()

