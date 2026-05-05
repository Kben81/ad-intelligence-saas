from pytrends.request import TrendReq

def get_trend(keyword):
    try:
        pytrends = TrendReq(hl="fr-FR", tz=360)
        pytrends.build_payload([keyword], timeframe="today 3-m")
        df = pytrends.interest_over_time()

        if df.empty:
            return 25

        return float(df[keyword].iloc[-1])

    except:
        return 25