import argparse
import common.config
import common.view
from src.order.args import OrderArguments

def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    parser.add_argument(
        "orderid",
        help=(
            "The ID of the Order to get. If prepended "
            "with an '@', this will be interpreted as a client Order ID"
        )
    )
    extnArgs=OrderArguments(parser)
    extnArgs.add_client_order_extensions()
    extnArgs.add_client_trade_extensions()

    args=parser.parse_args(["3"])
    api = args.config.create_context()

    extnArgs.parse_arguments(args)

    response=api.order.set_client_extensions(args.config.active_account,args.orderid,**extnArgs.parsed_args)

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    print(response.get('orderClientExtensionsModifyTransaction',200))

if __name__ == "__main__":
    main()