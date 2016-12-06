import os
from ref_mat import RefMat
from config import Config
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--files", type=str,
                    help="file or list of file (comma serpated) in Inbox for importing")
parser.add_argument("--libraries", type=str,
                    help="library or list of libraries (comma serpated) where symlink will be created")
parser.add_argument("--items", type=str,
                    help="item or list of items (comma serpated) where symlink will be created")


REFMAT_SYMLINK_DB = os.path.join(os.path.abspath('..'), 'db')


if __name__ == '__main__':
    args = parser.parse_args()
    ref_mat = RefMat(config=Config(root=REFMAT_SYMLINK_DB))
    ref_mat.import_files(
        files=[args.files],
        libraries=[args.libraries],
        items=[args.items]
    )
