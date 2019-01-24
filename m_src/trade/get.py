import argparse
import common.config
import common.view


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument('--trade-id', '-t')
    parser.add_argument('--all', '-a', action='store_true', default=False)
    parser.add_argument('--summary', '-s', action='store_true', default=True)
    parser.add_argument('--verbose', '-v', dest='summary', action='store_false')

    args = parser.parse_args('-a -v'.split())

    if args.trade_id is None and not args.all:
        parser.error("Must provide --trade-id or --all")

    account_id = args.config.active_account

    api = args.config.create_context()

    if args.all:
        response = api.trade.list_open(account_id)
        if not args.summary:
            print("-" * 80)
        for trade in reversed(response.get("trades", 200)):
            if args.summary:
                print(trade.title())
            else:
                print(trade.yaml(True))
                print("-" * 80)
        return

    if args.trade_id:
        response = api.trade.get(account_id, args.trade_id)
        trade = response.get("trade", 200)
        if args.summary:
            print(trade.title())
        else:
            print(trade.yaml(True))
        return


if __name__ == "__main__":
    main()
