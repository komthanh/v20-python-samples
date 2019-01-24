import argparse
import common.config
import common.view
from src.order.view import print_order_create_response_transactions


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument('tradeid')
    parser.add_argument('--units', default='ALL')

    args = parser.parse_args('5 --units 1'.split())

    account_id = args.config.active_account

    api = args.config.create_context()

    response = api.trade.close(account_id, args.tradeid, units=args.units)

    print(
        "Response: {} ({})\n".format(
            response.status,
            response.reason
        )
    )

    print_order_create_response_transactions(response)


if __name__ == "__main__":
    main()
