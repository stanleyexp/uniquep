import csv
import sys
sys.path.append('dragonmapper')
from dragonmapper import transcriptions, hanzi
from os import path
import re
from itertools import tee


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
def print_trie(node, word, level, print_list):
    if node.is_leaf:
        print('->' + '->'.join(print_list), end=' ')
        print(' ')
    for key, value, in node.nodes.items():
        print_trie(value, key, level+1, print_list + [key])

class TrieNode():
    def __init__(self):
        self.nodes: dict[str, TrieNode] = dict()
        self.is_leaf = False
        self.parent: TrieNode = None
    def insert(self, ipa_list, dict_leaf):
        curr = self
        for ipa_w in ipa_list:
            if ipa_w not in curr.nodes:
                child = TrieNode()
                child.parent = curr
                curr.nodes[ipa_w] = child
            curr = curr.nodes[ipa_w]
        curr.is_leaf = True
        dict_leaf[' '.join(ipa_list)] = curr

    # return tuple(int, str):
    def find_uniq(self, ipa_list, leaf_node):
        curr = leaf_node
        for ipa_w in ipa_list[::-1]:
            # if curr.parent == root
            if curr.parent is None:
                return 0, ipa_list[0]
            child_num = len(curr.parent.nodes.keys())
            if child_num > 1:
                return ipa_list.index(ipa_w), ipa_w
            curr = curr.parent 
     
# return dict[str, (int, str)]
def build_dic_uniq(lines):
    root = TrieNode()
    # dic[leaf_node, TrieNode]
    dict_leaf = dict()
    for _, col in enumerate(lines[:]):
        ipa = col[3].strip()
        root.insert(ipa.split(' '), dict_leaf)

    # print_trie(root, '', level=0, print_list=[])
    # return
    
    # dic[str, (uniq_ipa_index, uniq_ipa_ch)]
    dic_uniq = dict()
    for _, col in enumerate(lines[:]):
        ipa = col[3].strip()
        leaf_node = dict_leaf[ipa]
        dic_uniq[ipa] = root.find_uniq(ipa.split(' '), leaf_node)
        # print(dic_uniq[ipa])
        # print("=================================")
    return dic_uniq


def create_uniquep(input_file, output_file):

    current_dir = path.dirname(__file__)
    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)

    with open(input_file, 'r') as in_file:
        lines = (line.split(",") for line in in_file if line)
        # copy generator
        lines, lines_copy = tee(lines)
        dict_uniq = build_dic_uniq(list(lines_copy))
        with open(output_file, 'w') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            for index, col in enumerate(lines):
                try:
                    new_row = []
                    new_row.append(col[0])
                    new_row.append(col[1])
                    new_row.append(col[2].strip())
                    ipa = col[3].strip()
                    new_row.append(ipa)
                    uniq_tuple = dict_uniq[ipa]
                    uniq_index = uniq_tuple[0]
                    uniq_ch = uniq_tuple[1]
                    new_row.append(str(uniq_index).strip())
                    new_row.append(uniq_ch.strip())
                    writer.writerow(new_row)

                except Exception as e:
                    print(index)
                    print(col)
                    print(str(e))



def start():
    # txt_to_csv('cidian_zhzh-kfcd-2021714.txt',
    #     'cidian_zhzh-kfcd-2021714.csv')
    # ping_to_ipa('cidian_zhzh-kfcd-2021714.csv', 
    #     'cidian_zhzh-kfcd-2021714-ipa.csv')
    # ping_to_ipa('cidian_zhzh-kfcd-2021714.csv', 
    #     'cidian_zhzh-kfcd-2021714-no-notation-ipa.csv')
    
    # create_uniquep('cidian_zhzh-kfcd-2021714-no-notation-ipa.csv',
    #     'uniquep-no-notation-ipa.csv')
    create_uniquep('test.csv',
        'uniquep-no-notation-ipa.csv')

if __name__ == "__main__":
    start()