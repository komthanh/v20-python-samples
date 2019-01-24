import argparse
import common.config
import common.args


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument('fromid')
    parser.add_argument('toid')
    parser.add_argument('--type', action='append')

    args = parser.parse_args("1 60 --type".split() + ['MARKET_ORDER', '--type', 'LIMIT_ORDER'])
    # args = parser.parse_args("1 60 --type ORDER --type FUNDING".split())

    api = args.config.create_context()

    filter = None
    if args.type is not None:
        filter = ','.join(args.type)

    account_id = args.config.active_account

    response = api.transaction.range(account_id, fromID=args.fromid, toID=args.toid, type=filter)

    for transaction in response.get("transactions", 200):
        print(transaction.title())


if __name__ == "__main__":
    main()
