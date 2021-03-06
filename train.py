import re
import argparse
import pickle

import os
import ast
from collections import defaultdict

parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description='Creat a library for generate of sequence of words. After train.py use generate.py')
parser.add_argument('--input-dir', '-i', default='stdin', dest='input_dir', help='Way to collection of train_files, it will take only .txt files')

parser.add_argument('--model', '-m', type=argparse.FileType('wb'), default=open('model.pickle', 'wb'), help='Way to file for saving model. File extension is "*.pickle"')

parser.add_argument('--lc', action='store_true', help='To produce lowacase train files')
args = parser.parse_args()
    
def add_text_in_Lib(train_text, Lib):
    last_word = ''  #содержит последнее слово предыдущей строчки
    for line in train_text:
        Lib, last_word = add_line_in_Lib(line, Lib, last_word)
    return Lib
    
def add_line_in_Lib( line, Lib, last_word = ''):
    # вставим в начало строчки последнее слово предыдущей строчки
    line = last_word + ' ' + line 
    # приведем все символы к lowercase
    if (args.lc):
        line = line.lower()
    # оставим только алфавитные символы
    line = re.sub(r"[^a-zа-яA-ZА-Я' ]", '', line)
    # разделение строки по словам
    line_list = line.split()
    #зафиксируем последнее слово строчки
    if line_list:
        last_word = line_list[-1]
    #ввод пар строк в библиотеку
    for i in range(len(line_list) - 1):
        if line_list[i + 1] in Lib[line_list[i]]:
            Lib[line_list[i]][line_list[i + 1]] += 1
        else:
            Lib[line_list[i]][line_list[i + 1]] = 1
    return Lib, last_word

def main():    
    Lib = defaultdict(dict)       #библиотека пар слов
    if args.input_dir != 'stdin':
        pattern = re.compile(r'.*\.txt')
        train_list = [_file for _file in os.listdir(args.input_dir) if pattern.match(_file)]
        for _file in train_list:
            train_text = open(args.input_dir + _file, 'r', encoding="utf-8")
            Lib = add_text_in_Lib(train_text, Lib)
            train_text.close()
    else:
        train_text = ''
        while True:
            line = input()
            if not(line):
                break
            train_text += ' ' + line
        Lib = add_line_in_Lib(train_text, Lib)[0]
    #print('Lib: ', Lib, '\n')
    pickle.dump(Lib, args.model)
    print('ok')


if __name__ == '__main__':
    main()


