import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import json
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_broker_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, verify=False)
    
    response.encoding = 'big5' 
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', {'id': 'oMainTable'})
    
    data = []
    if table:
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                date = cols[0].text.strip()
                net_buy_sell = cols[4].text.strip()
                data.append({'日期': date, '買賣超': net_buy_sell})
    
    return pd.DataFrame(data)

def format_net_buy_sell(value):
    val = int(str(value).replace(',', ''))
    if val < 0:
        return f"({abs(val)})"
    return str(val)

def main():
    with open('brokers.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    all_data = []
    for stock_id, broker_list in config.items():
        for broker in broker_list:
            print(f"calling {stock_id} - {broker['name']}")
            df = get_broker_data(broker['url'])

            df = df.head(10)
            
            df['股票代號'] = stock_id
            df['券商名稱'] = broker['name']
            
            all_data.append(df)
            time.sleep(1)
    
    final_df = pd.concat(all_data, ignore_index=True).apply(format_net_buy_sell)
    final_df.to_csv('data/stock_data.csv', index=False, encoding='utf-8-sig')
    print("資料已儲存到 data/stock_data.csv")

if __name__ == "__main__":
    main()