from faslr.utilities import subset_dict

input_dict = {
    'a': [1, 2, 3],
    'b': [4, 5, 6],
    'c': [7, 9, 9]
}

dict_expectation = {
    'a': [1, 2, 3],
    'b': [4, 5, 6]
}

def test_subset_dict():
    dict_test = subset_dict(
        input_dict=input_dict,
        keys=['a', 'b']
    )

    assert dict_test == dict_expectation