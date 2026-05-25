import requests

def get_info():
    response = requests.get(url='https://yobit.net/api/3/info')
    with open('info.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response.text

def get_ticker(coin_symbol_1 = 'btc', coin_symbol_2 = 'usd'):
    response = requests.get(url=f'https://yobit.net/api/3/ticker/{coin_symbol_1}_{coin_symbol_2}?ignore_invalid=1')
    with open('ticker.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)
    return response.text

def get_depth(coin_symbol_1 = 'btc', coin_symbol_2 = 'usd', limit=150):
    response = requests.get(url=f'https://yobit.net/api/3/depth/{coin_symbol_1}_{coin_symbol_2}?limit={limit}&ignore_invalid=1')
    with open('depth.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)

    bids = response.json()[f"{coin_symbol_1}_{coin_symbol_2}"]["bids"]

    total_bids_amount = 0.0
    for price, coin_amount in bids:
        total_bids_amount += float(price) * float(coin_amount)

    return f"Total bids: {total_bids_amount:.1f} $"

def get_trades(coin_symbol_1='btc', coin_symbol_2='usd', limit=150):
    pair = f"{coin_symbol_1}_{coin_symbol_2}"
    url = f'https://yobit.net/api/3/trades/{pair}?limit={limit}&ignore_invalid=1'
    response = requests.get(url=url)
    with open('trades.txt', 'w', encoding='utf-8') as f:
        f.write(response.text)

    # 1) response.json() возвращает словарь { "pair": [ ... ] }
    data = response.json()
    trades_list = data[pair]  # вытаскиваем список сделок
    print(f"Total trades: {len(trades_list)}")

    total_trade_ask = 0.0
    total_trade_bid = 0.0
    for item in trades_list:
        # теперь item — словарь с ключами 'type', 'price', 'amount'
        if item['type'] == 'ask':
            total_trade_ask += item['price'] * item['amount']
        else:
            total_trade_bid += item['price'] * item['amount']

    info = (
        f"[-] TOTAL {coin_symbol_1.upper()} SELL: {total_trade_ask:.1f} $\n"
        f"[+] TOTAL {coin_symbol_1.upper()} BUY: {total_trade_bid:.1f} $"
    )
    return info




def main():
    info = get_info()

    ticker = get_ticker(coin_symbol_1='eth')
    print(ticker)

    depth = get_depth(coin_symbol_1='eth', coin_symbol_2='usd', limit=150)
    print(depth)

    trades = get_trades(coin_symbol_1='eth', coin_symbol_2='usd', limit=150)
    print(trades)


if __name__ == '__main__':
    main()

# Напиши подробно на русском как сделать мониторинг результатов отправляя запросы каждые 10, 20, 30  мин  или час, сохранять данные в BD и после сверять значения и как только произойдет резкое увеличение суммы следовательно пора закупаться  и отправлять сообщения через tg bot, что бы зайти и купить вручную. Для этого еще нужно создать переменную для баланса.
# Т.е. скупать ордера при посадке, а при увеличении стоимости на 5, 10, 20 % выставлять на продажу