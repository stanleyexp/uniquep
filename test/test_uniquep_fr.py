import pytest
from os import path

# @pytest.fixture
def csv_lines():
    current_dir = path.dirname(__file__)
    test_file = path.join(current_dir, "uniquep-Lexique-query-fr-test.csv")
    assert_file = path.join(current_dir, "Lexique-query-fr-test.csv")
    with open(test_file, 'r') as in_file1, open(assert_file, 'r') as in_file2:
        test_lines = (line.split(",") for line in in_file1 if line)
        assert_lines = (line.split(",") for line in in_file2 if line)
        # yield (test_lines, assert_lines)
        for index, (test_col, assert_col) in enumerate(zip(test_lines, assert_lines)):
            test_index = int(test_col[4].strip())
            assert_index = int(assert_col[4].strip())-1
            yield test_index, assert_index, test_col, assert_col
        

# pytest --maxfail=10 
# compare uniqueness point index
@pytest.mark.parametrize('test_index, assert_index, test_col, assert_col', csv_lines())
def test_uniquep_index(test_index, assert_index, test_col, assert_col):
    assert test_index == assert_index, f'\ntest: => {test_col[3]},{test_col[4]}\nassert: => {assert_col[3]},{assert_col[4]}'

