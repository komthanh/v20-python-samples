import sys

sys.path.append("/Users/thieut/Exercises/v20-python-samples/src")

import select
import argparse
import common.config
from src.account.account import Account


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    parser.add_argument("--poll-interval", type=int, default=5, help="Number of seconds between polls for account changes")
    args=parser.parse_args()

    account_id=args.config.active_account
    api=args.config.create_context()
    response=api.account.get(account_id)

    account = Account(response.get("account","200"))

    def dump():
        account.dump()
        print("Press <ENTER> to see current state of account {}".format(account.details.id))

    dump()

    while True:
        i,o,e=select.select([sys.stdin],[],[],args.poll_interval)
        if i:
            sys.stdin.readline()
            dump()

        response=api.account.changes(account_id,sinceTransactionID=account.details.lastTransactionID)
        account.apply_changes(response.get('changes','200'))
        account.apply_state(response.get('state','200'))
        account.details.lastTransactionID=response.get('lastTransactionID','200')

if __name__=='__main__':
    main()