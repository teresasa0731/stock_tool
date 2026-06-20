import streamlit as st
import pandas as pd
import json

st.title("券商買賣超資料查詢")
st.info("資料每日 18:30 自動更新，若需補抓資料請聯繫Sasa。")

# 讀取資料
df = pd.read_csv("data/stock_data.csv")
# 讀取 brokers.json 取得名稱對應 URL 的字典
with open('brokers.json', 'r', encoding='utf-8') as f:
    broker_config = json.load(f)

# 為了方便建立超連結，我們建立一個「名稱對 URL」的對照表
name_to_url = {}
for stock_id, brokers in broker_config.items():
    for b in brokers:
        name_to_url[b['name']] = b['url']

selected_stock = st.selectbox("請選擇股票", df['股票代號'].unique())
stock_df = df[df['股票代號'] == selected_stock]

# 轉置資料
pivot_df = stock_df.pivot(index='日期', columns='券商名稱', values='買賣超')
pivot_df = pivot_df.sort_index(ascending=False)

# 將欄位名稱改成 Markdown 連結
# 例如：將 "玉山-新莊" 改成 "[玉山-新莊](https://...)"
new_columns = []
for name in pivot_df.columns:
    url = name_to_url.get(name, "#") # 如果找不到連結就用 #
    new_columns.append(f"[{name}]({url})")

pivot_df.columns = new_columns

# 顯示表格 (Streamlit 的 st.markdown 可以渲染表格中的連結)
st.markdown(pivot_df.to_html(escape=False), unsafe_allow_html=True)