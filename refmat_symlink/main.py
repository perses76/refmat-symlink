import os
from ref_mat import RefMat
from config import Config
import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "tags",
    type=str,
    help="tags for imported items",
    nargs='+'
)

parser.add_argument(
    "--files",
    type=str,
    help="Items in Inbox for importing. Default: all items from inbox",
    nargs='*'
)


SOLUTION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REFMAT_SYMLINK_DB = os.path.join(SOLUTION_DIR, 'db')


def main():
    args = parser.parse_args()
    ref_mat = RefMat(config=Config(root=REFMAT_SYMLINK_DB))

    if args.files is None:
        files_for_import = ref_mat.get_all_inbox_items()

        if len(files_for_import) < 1:
            print('No items for import found')
            return

        print('List of items for import:')
        for it in ref_mat.get_all_inbox_items():
            print(it)
        res = input('Are you sure? (Y/n)')
        if res and res.lower() != 'y':
            return

    ref_mat.import_files(
        files=args.files,
        tags=args.tags
    )


if __name__ == '__main__':
    main()
    print('End')
