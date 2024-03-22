import pandas as pd
import yfinance as yf
from datetime import datetime
from pydantic import BaseModel


class Information(BaseModel):
  country: str | None = None
  currency: str | None = None
  longName: str | None = None
  symbol: str | None = None
  website: str | None = None
  zip: str | None = None
  totalCash: int | None = None
  totalDebt: int | None = None
  totalRevenue: int | None = None


def parse_date(data: dict) -> dict:
  """
  parse the timestamp inside the dictionary into date-str format
  """
  timestamp: pd.Timestamp = data['Date']
  data['Date'] =  timestamp.strftime('%Y-%m-%d')
  return data


def history(ticker_symbol: str,
            start_date: str | None = None,
            end_date: str | None = None) -> list[dict] | None:
  "get open and close prices in specific period from yahoo finance"

  if not start_date:
     start_date: str = '2022-01-01'
  if not end_date:
     end_date: str = datetime.now().strftime('%Y-%m-%d')

  ticker = yf.Ticker(ticker_symbol.upper())
  hist: pd.DataFrame | None = ticker.history(start=start_date, end=end_date)

  if not len(hist):
    return None
  
  hist = hist[['Open', 'Close']]
  hist = hist.reset_index()
  hist = hist.to_dict(orient='records')
  hist = list(map(parse_date, hist))

  return hist


def information(ticker_symbol: str) -> dict | None:
  """
  get basic information about ticker company
  """

  ticker: yf.Ticker = yf.Ticker(ticker_symbol.upper())
  data = ticker.get_info()

  if len(data) <= 1:
    return None
  
  data = Information(**data)

  return data.model_dump()


def main() -> None:
    aapl = history(ticker_symbol='aapl')
    print(aapl)
    aapl = history(ticker_symbol='aapl',
                   start_date='2024-03-01',
                   end_date='2024-03-22')
    print(aapl)
    

if __name__ == "__main__":
    main()