import argparse
import common.config
import common.args
from src.pricing.view import price_to_string
import time


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument('--instrument', '-i', type=common.args.instrument, required=True, action='append')
    parser.add_argument('--poll', '-p', action='store_true', default=False)
    parser.add_argument('--poll-interval', type=float, default=2)

    args = parser.parse_args("-i EUR_USD -i AUD_USD -p --poll-interval 1".split())
    account_id = args.config.active_account
    api = args.config.create_context()

    latest_price_time = None

    def poll(latest_price_time):
        response = api.pricing.get(account_id, instruments=",".join(args.instrument), since=latest_price_time, includeUnitsAvailable=True)
        for price in response.get('prices', 200):
            if latest_price_time is None or price.time > latest_price_time:
                print(price_to_string(price))
        for price in response.get("prices", 200):
            if latest_price_time is None or price.time > latest_price_time:
                latest_price_time = price.time
        return latest_price_time

    latest_price_time = poll(latest_price_time)

    while args.poll:
        time.sleep(args.poll_interval)
        latest_price_time = poll(latest_price_time)


if __name__ == "__main__":
    main()
