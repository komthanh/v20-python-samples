import argparse
import common.config
import common.view
import v20.transaction

def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument('tradeid')
    parser.add_argument('--client-id')
    parser.add_argument('--tag')
    parser.add_argument('--comment')

    args=parser.parse_args('52 --client-id cl_52 --tag extended_transaction --comment the_first_extended_transaction_I_requested'.split())

    if (args.client_id is None and args.tag is None and args.comment is None):
        parser.error("must provide at least one client extension to be set")

    clientExtensions=v20.transaction.ClientExtensions(id=args.client_id, comment=args.comment, tag=args.tag)

    api=args.config.create_context()

    account_id=args.config.active_account

    response=api.trade.set_client_extensions(account_id,args.tradeid,clientExtensions=clientExtensions)

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print(response.get('tradeClientExtensionsModifyTransaction',200))

if __name__ == "__main__":
    main()