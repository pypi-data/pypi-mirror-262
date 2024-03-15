import argparse
from arepo.db import DatabaseConnection
from arepo.utils import TABLE_NAMES
from arepo.models.data import DatasetModel


def main():
    parser = argparse.ArgumentParser("Dataset interaction commands")
    parser.add_argument('-u', '--uri', help='Database URI', required=True)
    subparsers = parser.add_subparsers(dest='subparser')
    init_parser = subparsers.add_parser('init', help='Initialize the database')
    list_parser = subparsers.add_parser('list', help='List content in tables')
    list_parser.add_argument('-t', '--table', choices=list(TABLE_NAMES.keys()), help='Table to list')
    list_parser.add_argument('-l', '--limit', type=int, help='Limit the number of entries', default=20)

    args = parser.parse_args()

    if args.subparser == 'init':
        DatabaseConnection.init(args.uri)

    if args.subparser == 'list':
        if args.limit < 1:
            print('Limit must be greater than 0.')
            return

        print('Getting database connection.')
        db = DatabaseConnection(args.uri)
        print('Getting session.')
        session = db.get_session(scoped=True)

        print(f'Querying {args.table}.')
        entries = session.query(TABLE_NAMES[args.table]).all()
        # keep the first 20 entries only
        if len(entries) > args.limit:
            entries = entries[:args.limit]
            print(f'Only the first {args.limit} entries are shown.')

        for entry in entries:
            print(entry.id, entry.name)

        session.close()

    db = DatabaseConnection(args.uri)
    session = db.get_session()
    dataset = session.query(DatasetModel).filter(DatasetModel.id == 30).first()
    commits = [c for v in dataset.vulnerabilities for c in v.commits]
    print(commits[0].repository)
