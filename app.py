import streamlit as st
import pandas as pd

st.title("券商買賣超資料")

df = pd.read_csv("data/stock_data.csv")

selected_stock = st.selectbox("請選擇股票", df['股票代號'].unique())
filtered_df = df[df['股票代號'] == selected_stock]

st.table(filtered_df)