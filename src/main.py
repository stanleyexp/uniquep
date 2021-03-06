import csv
from os import path
from dragonmapper import transcriptions
import re
from itertools import tee
import pdb

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

#  漢語拼音(教育部辭典) -> 漢語拚音+數字聲調
def pinyin1_to_pinyin2(input_file, output_file):
    current_dir = path.dirname(__file__)
    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)
    with open(input_file, 'r') as in_file:
        lines = (line.split(",") for line in in_file if line)
        with open(output_file, 'w') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            for index, col in enumerate(lines):
                try:
                    # ignore word without pinyin
                    if (col[2].strip() == ''):
                        continue
                    new_row = []
                    new_row.append(col[0])
                    new_row.append(col[1])
                    ping2 = transcriptions.accented_to_numbered2(convert(col[2]))
                    new_row.append(ping2.strip())
                    writer.writerow(new_row)

                except Exception as e:
                    print(index)
                    print(col)
                    print(str(e))


def pinyin_to_ipa(input_file, output_file, has_tone=False):
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
                    ipa = transcriptions.pinyin_to_ipa2(
                        convert(col[2], has_tone))
                    new_row.append(ipa.strip())
                    writer.writerow(new_row)

                except Exception as e:
                    print(index)
                    print(col)
                    print(str(e))


def convert(col_string, has_tone=False):

    col_list = col_string.split(" ")

    for index, col1 in enumerate(col_list):
        # replace v with ü
        if re.search(r'lv\d', col1):
            p2 = r'v' if has_tone else r'v\d'
            col_list[index] = re.sub(p2, 'ü', col1)
        elif re.search(r'nv\d', col1):
            p3 = r'v' if has_tone else r'v\d'
            col_list[index] = re.sub(p3, 'ü', col1)
        else:
            if not has_tone:
                col_list[index] = re.sub(r'\d', '', col1)

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
    def insert(self, ipa, ipa_list, dict_leaf):
        curr = self
        for ipa_w_index, ipa_w in enumerate(ipa_list):

            if ipa_w not in curr.nodes:
                child = TrieNode()
                child.parent = curr
                curr.nodes[ipa_w] = child

            if ipa_w_index == len(ipa_list)-1:
                curr = curr.nodes[ipa_w]
                child = TrieNode()
                child.parent = curr
                curr.nodes["$"] = child
                child.is_leaf = True
                curr = child
                break

            curr = curr.nodes[ipa_w]
        dict_leaf[ipa] = curr

    # return tuple(int, str):
    def find_uniq(self, ipa_list, leaf_node):
        curr = leaf_node
        ipa_list_last_index = len(ipa_list)-1
        # is end of word a uniqueness point
        child_num = len(curr.parent.nodes.keys())
        if child_num > 1:
            return ipa_list_last_index, ipa_list[-1]
        
        # move to end of word
        curr = curr.parent
        for index in range(ipa_list_last_index, -1, -1):
            if curr.parent is None:
                return 0, ipa_list[0]
            child_num = len(curr.parent.nodes.keys())
            if child_num > 1:
                return index, ipa_list[index]
            curr = curr.parent

    def find_uniq_tone(self, ipa_list, leaf_node):
        curr = leaf_node
        ipa_list_last_index = len(ipa_list)-1

        # is end of word a uniqueness point
        child_num = len(curr.parent.nodes.keys())
        if child_num > 1:
            # if uniqueness point is digit(tone)
            if (ipa_list[-1].isdigit()):
                return ipa_list_last_index-1, ipa_list[ipa_list_last_index-1] + ipa_list[ipa_list_last_index]
            # if uniqueness point is alphabet
            return ipa_list_last_index, ipa_list[-1]

        # move to end of word
        curr = curr.parent
        for index in range(ipa_list_last_index, -1, -1):
            # if curr.parent == root
            if curr.parent is None:
                return 0, ipa_list[0]
            child_num = len(curr.parent.nodes.keys())
            if child_num > 1:
                # return index is the index of alphabet and
                # uniqueness point = alphabet + digit(tone)
                
                # if uniqueness point is digit(tone)
                if (ipa_list[index].isdigit()):
                    return index-1, ipa_list[index-1] + ipa_list[index]
                # if uniqueness point is alphabet + digit(tone)
                if index < ipa_list_last_index and ipa_list[index+1].isdigit():
                    return index, ipa_list[index] + ipa_list[index+1]
                # if uniqueness point is alphabet
                return index, ipa_list[index]
            curr = curr.parent


def split_ipa(ipa):
    ipa_list = list(ipa)
    for index, ipa_ch in enumerate(ipa_list):
        if ipa_ch == ' ':
            ipa_list.remove(ipa_ch)
            continue
        if ipa_ch == 'ʰ':
            # merge
            ipa_list[index-1:index+1] = [''.join(ipa_list[index-1:index+1])]
        
    return  ipa_list

# return dict[str, (int, str)]
def build_dic_uniq(lines, has_tone):
    root = TrieNode()
    # dic[leaf_node, TrieNode]
    dict_leaf = dict()
    for _, col in enumerate(lines[:]):
        ipa = col[3].strip()
        root.insert(ipa, split_ipa(ipa), dict_leaf)

    # print_trie(root, '', level=0, print_list=[])

    # dic[str, (uniq_ipa_index, uniq_ipa_ch)]
    dic_uniq = dict()
    if not has_tone:
        for _, col in enumerate(lines[:]):
            ipa = col[3].strip()
            leaf_node = dict_leaf[ipa]
            dic_uniq[ipa] = root.find_uniq(split_ipa(ipa), leaf_node)
    else:  # has_tone=True
        for _, col in enumerate(lines[:]):
            ipa = col[3].strip()
            leaf_node = dict_leaf[ipa]
            dic_uniq[ipa] = root.find_uniq_tone(split_ipa(ipa), leaf_node)
    return dic_uniq


def create_uniquep(input_file, output_file, has_tone=False,
    current_dir=path.dirname(__file__)):

    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)

    with open(input_file, 'r') as in_file:
        lines = (line.split(",") for line in in_file if line)
        # copy generator
        lines, lines_copy = tee(lines)
        dict_uniq = build_dic_uniq(list(lines_copy), has_tone)
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
    # pinyin_to_ipa('cidian_zhzh-kfcd-2021714.csv', 
    #     'cidian_zhzh-kfcd-2021714-ipa.csv')
    # pinyin_to_ipa('cidian_zhzh-kfcd-2021714.csv', 
    #     'cidian_zhzh-kfcd-2021714-notune-ipa.csv')
    # create_uniquep('cidian_zhzh-kfcd-2021714-notune-ipa.csv',
    #     'uniquep-cidian_zhzh-kfcd-2021714-notune-ipa.csv')

    # pinyin1_to_pinyin2('dict_revised_2015_20211228-rawdata.csv',
    #     'dict_revised_2015_20211228.csv')
    # pinyin_to_ipa('dict_revised_2015_20211228.csv', 
    #     'dict_revised_2015_20211228-notune-ipa.csv')
    # pinyin_to_ipa('dict_revised_2015_20211228.csv', 
    #     'dict_revised_2015_20211228-ipa.csv', has_tone=True)
    # create_uniquep('dict_revised_2015_20211228-notune-ipa.csv',
    #     'uniquep-dict_revised_2015_20211228-notune-ipa.csv')
    create_uniquep('dict_revised_2015_20211228-ipa.csv',
        'uniquep-dict_revised_2015_20211228-ipa.csv', has_tone=True)

    
    # create_uniquep('test3.csv', 'test3-result.csv')

    # pinyin1_to_pinyin2('test2.csv','test2-result.csv')
    # pinyin_to_ipa('test1.csv','test1-result.csv', True)


if __name__ == "__main__":
    start()
