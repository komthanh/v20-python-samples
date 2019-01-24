import sys
sys.path.append("/Users/thieut/Exercises/v20-python-samples/src")

import argparse
import common.args
from order.view import print_order_create_response_transactions
import v20


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", default="api-fxpractice.oanda.com", help="v20 REST server hostname")
    parser.add_argument("--port", type=int, default=443, help="v20 REST server port")
    parser.add_argument("--accountid", default="101-001-8202252-001",
                        help="v20 account ID")
    parser.add_argument("--token", default="e8fee72913e5e218b36ae4e033799030-379435510d3d570855776d7ac80cd223",
                        help="v20 auth token")
    parser.add_argument("--instrument", default="EUR_USD", type=common.args.instrument, help="The instrument to place a market order for")
    parser.add_argument("--units", default="1", help="Number of units for the market order")
    args = parser.parse_args()

    api = v20.Context(args.hostname, args.port, token=args.token)

    response = api.order.market(args.accountid, instrument=args.instrument, units=args.units)

    print("Response: {} ({})".format(response.status, response.reason))
    print("")
    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
