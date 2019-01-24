import argparse
import common.config
import common.args
from src.pricing.view import price_to_string, heartbeat_to_string

def main():
    parser = argparse.ArgumentParser()
    common.config.add_argument(parser)

    parser.add_argument('--instrument','-i',type=common.args.instrument, required=True,action='append')
    parser.add_argument('--snapshot',action='store_true',default=True)
    parser.add_argument('--no-snapshot',dest='snapshot',action='store_false')
    parser.add_argument('--show-heartbeats','-s',action='store_true', default=False)

    args=parser.parse_args("-i EUR_USD".split())

    account_id=args.config.active_account

    api=args.config.create_streaming_context()

    response=api.pricing.stream(account_id,snapshot=args.snapshot,instruments=','.join(args.instrument))

    for msg_type, msg in response.parts():
        if msg_type == "pricing.Heartbeat" and args.show_heartbeats:
            print(heartbeat_to_string(msg))
        elif msg_type == "pricing.Price":
           print(price_to_string(msg))

if __name__=='__main__':
    main()