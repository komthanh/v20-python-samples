import sys
sys.path.append("/Users/thieut/Exercises/v20-python-samples/src")

import argparse
import common.config
from account.account import Account

def main():
    parser=argparse.ArgumentParser()
    common.config.add_argument(parser)
    args=parser.parse_args()
    account_id=args.config.active_account
    api=args.config.create_context()
    response=api.account.summary(account_id)
    account=Account(response.get("account","200"))
    account.dump()

if __name__=="__main__":
    main()