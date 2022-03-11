import csv
import sys
sys.path.append('dragonmapper')
from dragonmapper import transcriptions, hanzi
from os import path
import re


def txt_to_csv(input_file, output_file):
    current_dir = path.dirname(__file__)
    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)

    with open(input_file, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split("\t") for line in stripped if line)
        with open(output_file, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)


def ping_to_ipa(input_file, output_file):
    """
    current package: https://github.com/stanleyexp/dragonmapper
    another package: https://github.com/Connum/npm-pinyin2ipa
    """

    current_dir = path.dirname(__file__)
    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)

    with open(input_file, 'r') as in_file:
        lines = (line.split(",") for line in in_file if line)
        with open(output_file, 'w') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            for index, col in enumerate(lines):
                try:
                    new_row = []
                    new_row.append(col[0])
                    new_row.append(col[1])
                    new_row.append(col[2].strip())
                    ipa = transcriptions.pinyin_to_ipa(convert(col[2]))
                    new_row.append(ipa.strip())
                    writer.writerow(new_row)

                except Exception as e:
                    print(index)
                    print(col)
                    print(str(e))


def convert(col_string, has_notation=False):

    col_list = col_string.split(" ")

    for index, col1 in enumerate(col_list):
        # replace v with ü
        if re.search(r'lv\d', col1):
            p2 = r'v' if has_notation else r'v\d'
            col_list[index] = re.sub(p2, 'ü', col1)
        elif re.search(r'nv\d', col1):
            p3 = r'v' if has_notation else r'v\d'
            col_list[index] = re.sub(p3, 'ü', col1)
        else:
            if not has_notation:
                col_list[index] = re.sub(r'\d$', '', col1)

    return ' '.join(col_list)
"""
reference: https://github.com/TheAlgorithms/Python/blob/master/data_structures/trie/trie.py
"""
def print_trie(node, word):
    if node.is_leaf:
        print(word, end=' ')
    for key, value, in node.nodes.items():
        print(key)
        print_trie(value, key)

class TrieNode():
    def __init__(self):
        self.nodes: dict[str, TrieNode] = dict()
        self.is_leaf = False
    def insert(self, ipa_list):
        curr = self
        for ipa_w in ipa_list:
            if ipa_w not in curr.nodes:
                curr.nodes[ipa_w] = TrieNode()
            curr = curr.nodes[ipa_w]
        curr.is_leaf = True
        # for ipa in ipa_list:
        #     for ipa_ch in ipa:
        #         if ipa_ch not in curr.nodes:
        #             curr.nodes[ipa_ch] = TrieNode()
        #         curr = curr.nodes[ipa_ch]
        #     curr.is_leaf = True

    # return tuple(int, str):
    def find_uniq(self, ipa_list):
        curr = self
        print("ipa_list", ipa_list)
        for ipa_w in ipa_list:
            keys_list = list(curr.nodes.keys())
            child_num = len(keys_list)
            print("keys_list", keys_list)
            if child_num == 1:
                index = ipa_list.index(keys_list[0]) + 1
                print('ipa_list[index]', ipa_list[index])
                return index, ipa_list[index]
            elif curr.is_leaf:
                return 1,''
            curr = curr.nodes[ipa_w]

        # for index, ipa_ch in enumerate(ipa):
        #     child_num = len(curr.nodes.keys())
        #     if child_num == 1:
        #         return index, ipa[index+1]
        #     # elif child_num == 0:
        #     #     return index, ipa_ch
        #     curr = curr.nodes[ipa_ch]
# return dict[str, (int, str)]
def build_dic_uniq(lines):
    root = TrieNode()
    for _, col in enumerate(lines[:]):
        ipa = col[3].strip()
        root.insert(ipa.split(' '))
    print_trie(root, '')
    return
    # dic[str, (uniq_ipa_index, uniq_ipa_ch)]
    dic_uniq = dict()
    for _, col in enumerate(lines[:]):
        ipa = col[3].strip()
        dic_uniq[ipa] = root.find_uniq(ipa.split(' '))
        print(dic_uniq[ipa])
        print("=================================")
        # print("dic_uniq[ipa][0]", dic_uniq[ipa][0])
        # print("dic_uniq[ipa][1]", dic_uniq[ipa][1])
    return dic_uniq


def create_uniquep(input_file, output_file):

    current_dir = path.dirname(__file__)
    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)

    with open(input_file, 'r') as in_file:
        lines = (line.split(",") for line in in_file if line)
        dict_uniq = build_dic_uniq(list(lines))
        # with open(output_file, 'w') as out_file:
        #     writer = csv.writer(out_file, delimiter=',')
        #     for index, col in enumerate(lines):
        #         try:
        #             new_row = []
        #             new_row.append(col[0])
        #             new_row.append(col[1])
        #             new_row.append(col[2].strip())
        #             ipa = col[3].strip()
        #             new_row.append(ipa)
        #             uniq_tuple = dict_uniq[ipa]
        #             uniq_index = uniq_tuple[0]
        #             uniq_ch = uniq_tuple[1]
        #             new_row.append(str(uniq_index).strip())
        #             new_row.append(uniq_ch.strip())
        #             writer.writerow(new_row)

        #         except Exception as e:
        #             print(index)
        #             print(col)
        #             print(str(e))



def start():
    # txt_to_csv("cidian_zhzh-kfcd-2021714.txt',
    #     'cidian_zhzh-kfcd-2021714.csv')
    # ping_to_ipa("cidian_zhzh-kfcd-2021714.csv', 
    #     'cidian_zhzh-kfcd-2021714-ipa.csv')
    # ping_to_ipa('cidian_zhzh-kfcd-2021714.csv', 
    #     'cidian_zhzh-kfcd-2021714-no-notation-ipa.csv')
    
    # create_uniquep('cidian_zhzh-kfcd-2021714-no-notation-ipa.csv',
    #     'uniquep-no-notation-ipa.csv')
    create_uniquep('test.csv',
        'uniquep-no-notation-ipa.csv')

if __name__ == "__main__":
    start()