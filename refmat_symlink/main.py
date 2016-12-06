import os
from ref_mat import RefMat
from config import Config
import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "tags",
    type=str,
    help="library or list of libraries (comma serpated) where symlink will be created",
    nargs='+'
)

parser.add_argument(
    "--files",
    type=str,
    help="file or list of file (comma serpated) in Inbox for importing. If no files provided, all content of Inbox will be imported",
    nargs='*'
)


REFMAT_SYMLINK_DB = os.path.join(os.path.abspath('..'), 'db')


if __name__ == '__main__':
    args = parser.parse_args()
    ref_mat = RefMat(config=Config(root=REFMAT_SYMLINK_DB))
    ref_mat.import_files(
        files=args.files,
        tags=args.tags
    )
