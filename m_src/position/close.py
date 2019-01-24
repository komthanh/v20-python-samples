import argparse
import common.config
import common.view
import common.args
from order.view import print_order_create_response_transactions


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument('instrument', type=common.args.instrument)
    parser.add_argument('--long-units', default=None)
    parser.add_argument("--short-units", default=None)

    args = parser.parse_args("EUR_USD".split())

    account_id = args.config.active_account

    api = args.config.create_context()

    response = api.position.close(account_id, args.instrument, longUnits=args.long_units, shortUnits=args.short_units)

    print(
        "Response: {} ({})\n".format(
            response.status,
            response.reason
        )
    )

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
