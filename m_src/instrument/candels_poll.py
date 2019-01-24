import argparse
import common.config
import common.args
from datetime import datetime
import curses
import random
import time


class CandlePrinter():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        (h, w) = self.stdscr.getmaxyx()
        self.height = h
        self.width = w
        self.field_width = {'time': 19, 'price': 8, 'volume': 6}

    def set_instrument(self, instrument):
        self.instrument = instrument

    def set_granularity(self, granularity):
        self.granularity = granularity

    def set_candles(self, candles):
        self.candles = candles

    def update_candles(self, candles):
        new = candles[0]
        last = self.candles[-1]
        if new.time == last.time and new.volume == last.volume:
            return False
        self.candles[-1] = candles.pop(0)
        self.candles.extend(candles)
        self.candles = self.candles[-self.max_candle_count():]
        return True

    def max_candle_count(self):
        return self.height - 3

    def last_candle_time(self):
        return self.candles[-1].time

    def render(self):
        title = "{} ({})".format(self.instrument, self.granularity)
        header = (
            "{:<{width[time]}} {:<{width[price]}} "
            "{:>{width[price]}} {:>{width[price]}} {:>{width[price]}} "
            "{:<{width[volume]}}"
        ).format(
            "Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            width=self.field_width
        )
        x = int((len(header) - len(title)) / 2)
        self.stdscr.addstr(
            0,
            x,
            title,
            curses.A_BOLD
        )
        self.stdscr.addstr(2, 0, header, curses.A_UNDERLINE)
        y = 3

        for candle in self.candles:
            time = candle.time.split(".")[0]
            volume = candle.volume
            for price in ['mid', 'bid', 'ask']:
                c = getattr(candle, price, None)
                if c is None:
                    continue
                candle_str = (
                    "{:>{width[time]}} {:>{width[price]}} "
                    "{:>{width[price]}} {:>{width[price]}} "
                    "{:>{width[price]}} {:>{width[volume]}}"
                ).format(
                    time, c.o, c.h, c.l, c.c, volume, width=self.field_width
                )
                self.stdscr.addstr(y, 0, candle_str)
                y += 1
                break
        self.stdscr.move(0, 0)
        self.stdscr.refresh()


def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)
    parser.add_argument("--instrument", type=common.args.instrument, default='EUR_USD', help="The instrument to get candles for")
    parser.add_argument("--granularity", default=None, help="The candles granularity to fetch")
    args = parser.parse_args()
    account_id = args.config.active_account
    api = args.config.create_context()

    def poll_candles(stdscr):
        kwargs = {}

        if args.granularity is not None:
            kwargs["granularity"] = args.granularity

        printer = CandlePrinter(stdscr)
        kwargs["count"] = printer.max_candle_count()

        response = api.instrument.candles(args.instrument, **kwargs)

        if response.status != 200:
            print(response)
            print(response.body)
            return

        instrument = response.get("instrument", 200)
        granularity = response.get("granularity", 200)
        printer.set_instrument(instrument)
        printer.set_granularity(granularity)
        printer.set_candles(response.get("candles", 200))
        printer.render()
        while True:
            time.sleep(1)
            kwargs = {
                'granularity': granularity,
                'fromTime': printer.last_candle_time()
            }
            response = api.instrument.candles(args.instrument, **kwargs)
            candles = response.get('candles', 200)
            if printer.update_candles(candles):
                printer.render()

    curses.wrapper(poll_candles)


if __name__ == "__main__":
    main()
