import argparse
import common.config
import common.view

def main():
    parser=argparse.ArgumentParser()
    common.config.add_argument(parser)
    args=parser.parse_args()
    account_id=args.config.active_account
    api=args.config.create_context()
    response=api.account.instruments(account_id)
    instruments=response.get("instruments",'200')
    instruments.sort(key=lambda i: i.name)

    def margin_format(instrument):
        return "{:.0f}:1 ({})".format(1.0/float(instrument.marginRate), instrument.marginRate)

    def pip_format(instrument):
        location=float(10**instrument.pipLocation)
        return "{:.4f}".format(location)

    common.view.print_collection(
        "{} instruments".format(len(instruments)),
        instruments,
        [("Name",lambda i: i.name),("Type",lambda i: i.type),("Pip",pip_format),("Margin Rate",margin_format)]
    )

if __name__=="__main__":
    main()