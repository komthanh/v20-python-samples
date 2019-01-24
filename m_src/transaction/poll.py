import argparse
import common.config
import common.args
import time


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    parser.add_argument('--poll-interval', type=float, default=2)

    args = parser.parse_args('--poll-interval 0.1'.split())

    api = args.config.create_context()
    account_id = args.config.active_account
    response = api.account.summary(account_id)
    last_transaction_id = response.get('lastTransactionID', 200)
    last_transaction_id = 60 # manual override to test this method

    while True:
        time.sleep(args.poll_interval)
        response = api.transaction.since(account_id, id=last_transaction_id)
        for transaction in response.get("transactions", 200):
            print(transaction.title())
        last_transaction_id = response.get("lastTransactionID", 200)


if __name__ == "__main__":
    main()
