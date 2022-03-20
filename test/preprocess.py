import csv

import sys
from os import path, getcwd
from os.path import join, dirname
sys.path.append(join(dirname(getcwd()), "src"))
from main import create_uniquep
import eng_to_ipa

def pre_process_fr(input_file, output_file, has_tone=False):

    current_dir = path.dirname(__file__)
    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)

    with open(input_file, 'r') as in_file:
        lines = (line.split(",") for line in in_file if line)
        with open(output_file, 'w') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            for index, col in enumerate(lines):
                try:
                    # remove row puphon=0
                    if col[4].strip() == '0':
                        continue
                    new_row = []
                    new_row.append(col[0])
                    new_row.append(col[1])
                    new_row.append(col[2])
                    new_row.append(col[3].strip())
                    new_row.append(col[4].strip())
                    writer.writerow(new_row)

                except Exception as e:
                    print(index)
                    print(col)
                    print(str(e))

def pre_process_en(input_file, output_file, has_tone=False):

    current_dir = path.dirname(__file__)
    input_file = path.join(current_dir, input_file)
    output_file = path.join(current_dir, output_file)

    with open(input_file, 'r') as in_file:
        lines = (line.split(",") for line in in_file if line)
        with open(output_file, 'w') as out_file:
            writer = csv.writer(out_file, delimiter=',')
            for index, col in enumerate(lines):
                try:
                    # remove row puphon=0
                    if col[4].strip() == '0':
                        continue
                    new_row = []
                    new_row.append(col[0])
                    new_row.append(col[1])
                    new_row.append(col[2])
                    # convert to IPA
                    ipa = eng_to_ipa.convert(col[3].strip())
                    new_row.append(ipa)
                    new_row.append(col[4].strip())
                    writer.writerow(new_row)

                except Exception as e:
                    print(index)
                    print(col)
                    print(str(e))


if __name__ == "__main__":
    # pre_process_fr("Lexique-query-fr-rawdata.csv", "Lexique-query-fr-test.csv")
    # create_uniquep("Lexique-query-fr-test.csv",
    #     "uniquep-Lexique-query-fr-test.csv", current_dir=path.dirname(__file__))
    
    pre_process_en("aelp-en-rawdata.csv", "aelp-en-test.csv")
    # create_uniquep("aelp-en-test.csv",
    #     "uniquep-aelp-en-test.csv", current_dir=path.dirname(__file__))