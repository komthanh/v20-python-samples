import argparse
import common.config
import common.args
from instrument.view import CandlePrinter
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    parser.add_argument("--instrument", type=common.args.instrument, default="EUR_USD", help="The instrument to get candles for")
    parser.add_argument("--mid", action="store_true", help="Get mid-point based candles")
    parser.add_argument("--bid", action="store_true", help="Get bid based candles")
    parser.add_argument("--ask", action="store_true", help="Get ask based candles")
    parser.add_argument("--smooth", action="store_true", help="Smooth the candles")
    parser.set_defaults(mid=False, bid=False, ask=False)
    parser.add_argument("--granularity", default=None, help="Candle granularity to fetch")
    parser.add_argument("--count", default=None, help="Number of candles to fetch")
    date_format = "%Y-%m-%d %H:%M:%S"
    parser.add_argument("--from-time", default=None, type=common.args.date_time(), help="Start date of candles to be fetched")
    parser.add_argument("--to-time", default=None, type=common.args.date_time(), help="End date of candles to be fetched")
    parser.add_argument("--alignment-timezone", default=None, help="Timezone used to align daily candles")

    args = parser.parse_args()
    account_id = args.config.active_account
    api = args.config.create_context()

    kwargs = {}

    if args.granularity is not None:
        kwargs["granularity"] = args.granularity
    if args.smooth is not None:
        kwargs["smooth"] = args.smooth
    if args.count is not None:
        kwargs["count"] = args.count
    if args.from_time is not None:
        kwargs["fromTime"] = api.datetime_to_str(args.fromtime)
    if args.to_time is not None:
        kwargs["toTime"] = api.datetime_to_str(args.to_time)
    if args.alignment_timezone is not None:
        kwargs["alignmentTimezone"] = args.alignment_timezone

    price = "mid"

    if args.mid:
        kwargs["price"] = "M" + kwargs.get("price", "")
        price = "mid"
    if args.bid:
        kwargs["price"] = "B" + kwargs.get("price", "")
        price = "bid"
    if args.ask:
        kwargs["price"] = "A" + kwargs.get("price", "")
        price = "ask"

    response = api.instrument.candles(args.instrument, **kwargs)

    if response.status != 200:
        print(response)
        print(response.body)
        return

    print("Instrument: {}".format(response.get("instrument",200)))
    print("Granularity: {}".format(response.get("granularity",200)))

    printer=CandlePrinter()
    printer.print_header()

    candles=response.get("candles",200)

    for candle in candles:
        printer.print_candle(candle)

if __name__=="__main__":
    main()