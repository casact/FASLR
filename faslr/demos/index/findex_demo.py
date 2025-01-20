"""
Demo of the FIndex class. Initializes an FIndex object from the first index in the sample database.
"""
from faslr.demos.sample_db import set_sample_db

from faslr.index import FIndex

set_sample_db()

test_index = FIndex(from_id=1)

print(test_index.df)

test_index.meta_dict