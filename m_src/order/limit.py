import argparse
import common.config
from src.order.args import OrderArguments, add_replace_order_id_argument
from src.order.view import print_order_create_response_transactions

def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    add_replace_order_id_argument(parser)

    orderArgs = OrderArguments(parser)
    orderArgs.add_instrument()
    orderArgs.add_units()
    orderArgs.add_price()
    orderArgs.add_time_in_force()
    orderArgs.add_position_fill()
    orderArgs.add_take_profit_on_fill()
    orderArgs.add_stop_loss_on_fill()
    orderArgs.add_trailing_stop_loss_on_fill()
    orderArgs.add_client_order_extensions()
    orderArgs.add_client_trade_extensions()

    args = parser.parse_args("EUR_USD 1 1.16".split())
    api = args.config.create_context()
    orderArgs.set_datetime_formatter(lambda dt: api.datetime_to_str(dt))
    orderArgs.parse_arguments(args)

    if args.replace_order_id is not None:
        response=api.order.limit_replace(args.config.active_account, args.replace_order_id, **orderArgs.parsed_args)
    else:
        response=api.order.limit(args.config.active_account,**orderArgs.parsed_args)

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print_order_create_response_transactions(response)

if __name__ == "__main__":
    main()