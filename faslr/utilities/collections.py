def subset_dict(input_dict: dict, keys: list) -> dict:
    """
    Given an input dictionary and a list of desired keys, return a subset dictionary containing only those keys.
    :param input_dict:
    :param keys:
    :return:
    """
    idx_dict = {k: input_dict[k] for k in keys}

    return idx_dict
