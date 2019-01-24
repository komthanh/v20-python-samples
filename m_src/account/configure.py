import sys
import select
import argparse
import common.config
from common.view import print_response_entity
from account.account import Account

def main():
    parser=argparse.ArgumentParser()
    common.config.add_argument(parser)
    parser.add_argument("--margin-rate",default=None,help="New default margin rate for the account")
    parser.add_argument("--alias",default="Tai khoan giao dich",help="New alias for the account")

    args=parser.parse_args()
    account_id=args.config.active_account
    api=args.config.create_context()

    kwargs={}
    if args.alias is not None:
        kwargs["alias"]=args.alias
    if args.margin_rate is not None:
        kwargs["marginRate"]=args.margin_rate

    response=api.account.configure(account_id,**kwargs)

    if response.status==200:
        print("Success\n")

    print_response_entity(response,"200","Configure transaction","configureTransaction")

if __name__=="__main__":
    main()