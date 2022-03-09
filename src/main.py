import csv
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
    current package: https://github.com/tsroten/dragonmapper
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
                    col_2_no_notation = col[2]
                    ipa = transcriptions.pinyin_to_ipa(
                        convert(col_2_no_notation))
                    new_row.append(ipa.strip())
                    writer.writerow(new_row)

                except Exception as e:
                    print(index)
                    print(col)
                    print(str(e))

def convert(col_string):
    """"
    yo->yao
    lv->lyu
    nv->nyu
    ei->e 
    dia->dya
    """
    col_list = col_string.split(" ")

    for index, col1 in enumerate(col_list):
        
        if re.search(r'yo\d', col1):
            col_list[index] = re.sub(r'yo', 'yao', col1)
        elif re.search(r'lv\d', col1):
            col_list[index] = re.sub(r'lv', 'lyu', col1)
        elif re.search(r'nv\d', col1):
            col_list[index] = re.sub(r'nv', 'nyu', col1)
        elif re.search(r'ei\d', col1):
            col_list[index] = re.sub(r'ei', 'e', col1)
        elif re.search(r'dia\d', col1):
            col_list[index] = re.sub(r'dia', 'dya', col1)

    return ' '.join(col_list)
    
def start():
    # txt_to_csv("cidian_zhzh-kfcd-2021714.txt", "cidian_zhzh-kfcd-2021714.csv")
    ping_to_ipa("cidian_zhzh-kfcd-2021714.csv", 
        "cidian_zhzh-kfcd-2021714-ipa.csv")

    # parse
    # analyze
    # output csv

if __name__ == "__main__":
    start()