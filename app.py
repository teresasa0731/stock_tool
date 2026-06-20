import streamlit as st
import pandas as pd
import json

st.markdown("""
<style>
.red-neg { color: red; }
.gray-nan { color: #cccccc; } /* 灰色 */
</style>
""", unsafe_allow_html=True)

def format_cell(val):
    s = str(val)
    if pd.isna(val):
        return '<span class="gray-nan">-</span>'
    if '(' in s:
        return f'<span class="red-neg">{s}</span>'
    return s

# 3. 讀取並處理資料
df = pd.read_csv("data/stock_data.csv")
with open('brokers.json', 'r', encoding='utf-8') as f:
    broker_config = json.load(f)

# 建立名稱到 URL 的映射
name_to_url = {b['name']: b['url'] for stock_id, brokers in broker_config.items() for b in brokers}

selected_stock = st.selectbox("請選擇股票", df['股票代號'].unique())
stock_df = df[df['股票代號'] == selected_stock]
pivot_df = stock_df.pivot(index='日期', columns='券商名稱', values='買賣超').sort_index(ascending=False)

# 4. 將 pivot_df 轉換為 HTML 並加入連結與顏色
# 我們遍歷每一欄，手動加上 HTML 標籤
html_table = pivot_df.copy()
for col in html_table.columns:
    url = name_to_url.get(col, "#")
    # 將欄位名稱加上超連結
    new_col_name = f'<a href="{url}" target="_blank">{col}</a>'
    
    # 格式化資料：將負數轉紅
    html_table[col] = html_table[col].apply(lambda x: format_cell(x))
    
    # 重新命名欄位 (這裡用暫時的 key)
    html_table = html_table.rename(columns={col: new_col_name})

# 顯示表格
st.write(html_table.to_html(escape=False), unsafe_allow_html=True)