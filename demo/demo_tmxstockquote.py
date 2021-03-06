# To make print working for Python2/3
from __future__ import print_function

import tmxstockquote as tmx


def _main():
    print(tmx._str_to_float("34.50"))
    print(tmx._str_to_float("1,300,400.52"))
    print(tmx._str_to_float(""))
    print(tmx._str_to_float("N/A"))
    print("")

    print(tmx._yahoo_to_tmx_stock_name("CP.TO"))
    print(tmx._yahoo_to_tmx_stock_name("AP-UN.TO"))
    print(tmx._yahoo_to_tmx_stock_name("MMM"))
    print("")

    print(tmx._download_tmx_page('XBB.TO')[0:2])
    print("")

    for s in ["NA.TO", "XBB.TO", "AP-UN.TO", "BRK-A", "AAPL"]:
        print("=============================================")
        print("s: {}".format(s))

        print("get_name: {}".format(tmx.get_name(s)))
        print("get_price: {}".format(tmx.get_price(s)))
        print("get_change: {}".format(tmx.get_change(s)))
        print("get_volume: {}".format(tmx.get_volume(s)))
        print("get_stock_exchange: {}".format(tmx.get_stock_exchange(s)))
        print("get_market_cap: {}".format(tmx.get_market_cap(s)))
        print("get_dividend_yield: {}".format(tmx.get_dividend_yield(s)))
        print("get_price_earnings_ratio: {}".format(tmx.get_price_earnings_ratio(s)))
        print("get_price_book_ratio: {}".format(tmx.get_price_book_ratio(s)))

        print("get_52_week_low: {}".format(tmx.get_52_week_low(s)))
        print("get_52_week_high: {}".format(tmx.get_52_week_high(s)))
        print("get_currency: {}".format(tmx.get_currency(s)))


if __name__ == '__main__':
    _main()
