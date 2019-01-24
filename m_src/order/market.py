import argparse
import common.config
from src.order.args import OrderArguments
from src.order.view import print_order_create_response_transactions

def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    marketOrderArgs =OrderArguments(parser)
    marketOrderArgs.add_instrument()
    marketOrderArgs.add_units()
    marketOrderArgs.add_time_in_force(["FOK","IOC"])
    marketOrderArgs.add_price_bound()
    marketOrderArgs.add_position_fill()
    marketOrderArgs.add_take_profit_on_fill()
    marketOrderArgs.add_stop_loss_on_fill()
    marketOrderArgs.add_trailing_stop_loss_on_fill()
    marketOrderArgs.add_client_order_extensions()
    marketOrderArgs.add_client_trade_extensions()

    args=parser.parse_args("EUR_USD 1".split())
    api = args.config.create_context()

    marketOrderArgs.parse_arguments(args)

    response=api.order.market(args.config.active_account,**marketOrderArgs.parsed_args)

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print_order_create_response_transactions(response)

if __name__ == "__main__":
    main()