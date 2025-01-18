import os
import subprocess

from faslr.constants import (
    ROOT_PATH,
    SAMPLE_DB_DEFAULT_PATH
)


from faslr.index import FIndex

if os.path.exists(SAMPLE_DB_DEFAULT_PATH):
    pass
else:
    subprocess.run(['python', ROOT_PATH + '/samples/db/generate_sample_db.py'])

test_index = FIndex(from_id=1, db=SAMPLE_DB_DEFAULT_PATH)

print(test_index.df)