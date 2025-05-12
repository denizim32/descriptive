import streamlit as st
import pandas as pd
from betim import descriptive_stats  # kendi dosyanı import et

st.title("Betimleyici İstatistik Hesaplayıcı")

uploaded_file = st.file_uploader("Bir Excel veya CSV dosyası yükleyin", type=['csv', 'xlsx'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.write("Yüklenen veri:")
    st.dataframe(df)

    st.write("Betimleyici istatistikler:")
    stats_df = descriptive_stats(df)
    st.dataframe(stats_df)
