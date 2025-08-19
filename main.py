import requests
import os
from time import sleep


def get_moex_stock_price(ticker):
    url = f"http://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{ticker}.json?iss.only" \
          f"=marketdata&marketdata.columns=SECID,LAST&iss.meta=off"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        market_data = data['marketdata']['data']
        if market_data:
            return market_data[0][1]
    except requests.exceptions.RequestException as e:
        print(f"Ah shit, here we gone again!\n{e}")
        return None


def get_ticker_from_file():
    try:
        with open('tickers.txt', 'r') as t:
            return [line.strip().upper() for line in t.read().split('\n')]
    except FileNotFoundError:
        with open('tickers.txt', 'w'):
            print('Your list is empty!')
            return []


def get_tickers_info():
    [print(f'{ticket}: {get_moex_stock_price(ticket.upper())}')
     for ticket in get_ticker_from_file()
     if ticket.strip() != '']


def write_new(ticker):
    if ticker.upper() in get_ticker_from_file():
        print('This ticker in list now!')
    else:
        with open('tickers.txt', 'a') as t:
            t.write(ticker.upper())
        print('A ticker has been added')


def del_ticker(ticker):
    tickers = get_ticker_from_file()
    if ticker.upper() not in tickers:
        print('This ticker out of list')
    else:
        with open('tickers.txt', 'w') as data:
            [data.write(f'{t}\n') for t in tickers if t != ticker.upper()]
        print('A ticker has been deleted')


def open_list():
    file_path = "tickers.txt"
    os.system(f"notepad {file_path}")


def main():
    print('Welcome')
    sleep(1)
    print('write tickers in your file and push start')
    sleep(1)
    while True:
        match input('Do you want to start pars info? y/n:\t'):
            case 'y':
                get_tickers_info()
            case 'n':
                match input(
                    'Do you want:\n\t'
                    'write new tickers "-w"\n\t'
                    'del older "-d"\n\t'
                    'open list "-o"\n\t'
                    'exit "-e"\n\t'
                    'press enter for return\n:'
                ):
                    case '-o':
                        open_list()
                    case '-w':
                        write_new(input('enter new ticker:\t'))
                    case '-d':
                        del_ticker(input('enter ticker to del:\t'))
                    case '-e':
                        exit(0)
                    case '':
                        continue
                    case _:
                        print('Invalid commands')


if __name__ == '__main__':
    main()
