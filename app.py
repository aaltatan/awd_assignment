from stockapp.controllers import history
import re


def infinite_loop(input_msg: str, 
                  regex: re.Pattern, 
                  error_msg: str, 
                  optional: bool = False) -> str | None:
  
  "put the user in infinite loop until he gives valid values"
  'registration'

  inputted: str = ''
  while True:
    inputted = input(input_msg)
    if not inputted and optional:
      return None
    if not regex.search(inputted):
      print(f'\n{error_msg}\n')
    else:
      break
  return inputted


def get_args() -> dict[str, str | None]:

  "get valid user's inputs"

  date_regex: re.Pattern = re.compile(r'^20\d{2}-[0-1]\d-[0-3]\d')
  data: dict = {
    'symbol': {
      'input_msg': 'Please provide me ticker symbol which you want to get data about [ticker symbol]: ',
      'regex': re.compile(r'^[A-z\.:\-]{3,20}$'),
      'error_msg': 'Enter a valid ticker symbol please, like: "AMZN", "AAPL", ...',
      'optional': False,
    },
    'start_date': {
      'input_msg': 'Please provide me start date (press Enter to skip) [YYYY-MM-DD]: ',
      'regex': date_regex,
      'error_msg': 'Enter a valid date like: "2022-01-01" ',
      'optional': True,
    },
    'end_date': {
      'input_msg': 'Please provide me end date (press Enter to skip) [YYYY-MM-DD]: ',
      'regex': date_regex,
      'error_msg': 'Enter a valid date like: "2022-01-01" ',
      'optional': True,
    },
  }

  text: str = ' Welcome to yfinance tracker CLI Application '
  greeting_msg: str = text.center(len(text) + 40, '#')

  print(greeting_msg)

  ticker_symbol: str = infinite_loop(**data['symbol'])
  start_date: str | None = infinite_loop(**data['start_date'])
  end_date: str | None = infinite_loop(**data['end_date'])

  return {
    'ticker_symbol': ticker_symbol,
    'start_date': start_date,
    'end_date': end_date
  }


def main() -> None:
  user_inputs: dict = get_args()
  print('\nThanks for giving us from your time\nyou did give us the following data:\n')
  print('-' * 70)
  print(user_inputs)
  print('-' * 70)
  print('\nfetching data from yahoo finance, it may take a while, please wait ...\n')
  hist: list[dict] = history(**user_inputs)
  if hist:
    for row in hist:
      print(row)


if __name__ == "__main__":
  main()