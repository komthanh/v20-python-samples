import argparse
import common.config
from src.order.args import OrderArguments, add_replace_order_id_argument
from src.order.view import print_order_create_response_transactions

def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    add_replace_order_id_argument(parser)

    orderArgs =OrderArguments(parser)
    orderArgs.add_trade_id()
    orderArgs.add_price()
    orderArgs.add_time_in_force(["GTD",'GFD','GTC'])
    orderArgs.add_client_order_extensions()

    args = parser.parse_args("7 1.163".split())

    api = args.config.create_context()

    orderArgs.parse_arguments(args)

    if args.replace_order_id is not None:
        response=api.order.take_profit_replace(args.config.active_account,args.replace_order_id,**orderArgs.parsed_args)
    else:
        response=api.order.take_profit(args.config.active_account,**orderArgs.parsed_args)

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()

