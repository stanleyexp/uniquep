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
            # writer.writerow(('[繁體字]', '[簡體字]', '[漢語拼音]'))
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
    """"
    yo->yao
    lv->lyu
    nv->nyu
    ei->e 
    dia->dya
    """
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
    
def start():
    # txt_to_csv("cidian_zhzh-kfcd-2021714.txt",
    #     "cidian_zhzh-kfcd-2021714.csv")
    # ping_to_ipa("cidian_zhzh-kfcd-2021714.csv", 
    #     "cidian_zhzh-kfcd-2021714-ipa.csv")
    ping_to_ipa("cidian_zhzh-kfcd-2021714.csv", 
        "cidian_zhzh-kfcd-2021714-no-notation-ipa.csv")

    # parse
    # analyze
    # output csv

if __name__ == "__main__":
    start()