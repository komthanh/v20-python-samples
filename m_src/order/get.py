import argparse
import common.config
import common.view

def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    parser.add_argument('--orderid', default='5')
    args = parser.parse_args()
    api = args.config.create_context()

    response=api.order.get(args.config.active_account, args.orderid)

    print("Response: {} ({})".format(response.status, response.reason))
    print("")

    order=response.get('order',200)
    print(order)

if __name__ == "__main__":
    main()