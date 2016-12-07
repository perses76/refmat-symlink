import os
from ref_mat import RefMat
from config import Config
import argparse


parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument(
    "--db",
    type=str,
    help="Path to refmatdb. Default: ~/refmatdb",
    default=os.path.join(os.path.expanduser('~'), 'refmatdb'),
)

subparsers = parser.add_subparsers(help='sub-command help', dest="command")

parser_import = subparsers.add_parser('import', help='Import files from Inbox')
parser_initializedb = subparsers.add_parser('initialize', help='Initialize Refmat DB')

parser_import.add_argument(
    "tags",
    type=str,
    help="tags for imported items",
    nargs='+'
)

parser_import.add_argument(
    "--files",
    type=str,
    help="Items in Inbox for importing. Default: all items from inbox",
    nargs='*'
)


SOLUTION_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REFMAT_SYMLINK_DB = os.path.join(SOLUTION_DIR, 'db')


def main():
    args = parser.parse_args()
    print(args)
    ref_mat = RefMat(config=Config(root=args.db))
    if args.command == 'initialize':
        ref_mat.initializedb()
        print('The refmat was successfully initialized here: {}'.format(args.db))
        return
    if args.command == 'import':
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
        return


if __name__ == '__main__':
    main()
    print('End')
