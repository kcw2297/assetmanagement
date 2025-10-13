import yfinance


class VIXStrategy():
    def index(self) -> float:
        vix = yfinance.Ticker("^VIX")
        data = vix.history(period="1d")
        return float(data['Close'].iloc[-1])