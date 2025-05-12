import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Sayfa ayarları
st.set_page_config(page_title="Tanımlayıcı İstatistikler", layout="wide")
st.title("📊 Gelişmiş Tanımlayıcı (Betimleyici) İstatistik Uygulaması")

# Renk teması
theme = st.selectbox("🎨 Tema seçin", [ "dark", "whitegrid", "ticks"])
sns.set_theme(style=theme)

# Excel yükleme
uploaded_file = st.file_uploader("📂 Excel dosyanızı yükleyin", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("🔍 Veri Önizleme")
    st.dataframe(df.head())

    # Eksik verileri yönet
    st.write("🧩 Eksik Değer Sayıları:")
    st.write(df.isnull().sum())

    fill_method = st.radio("Eksik verilerle nasıl işlem yapılsın?", ["Boş bırak (NaN)", "0 ile doldur", "Satırı sil"])
    if fill_method == "0 ile doldur":
        df = df.fillna(0)
    elif fill_method == "Satırı sil":
        df = df.dropna()

    # Otomatik veri tipi tanıma
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Sayısal analiz
    st.subheader("📈 Sayısal Değişken Analizi")
    selected_nums = st.multiselect("Sayısal sütunları seçin:", numeric_cols)

    stats_output = {}

    if selected_nums:
        stats = df[selected_nums].describe().T
        stats["mod"] = df[selected_nums].mode().iloc[0]
        st.dataframe(stats)
        stats_output["Sayısal İstatistikler"] = stats

        for col in selected_nums:
            st.markdown(f"### 🔸 {col}")
            fig1, ax1 = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax1)
            ax1.set_title(f"{col} - Histogram")
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df[col], ax=ax2)
            ax2.set_title(f"{col} - Boxplot")
            st.pyplot(fig2)

    # Korelasyon Matrisi
    if st.checkbox("📌 Korelasyon matrisini göster"):
        st.subheader("🔗 Korelasyon Matrisi")
        corr = df[numeric_cols].corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr)
        st.pyplot(fig_corr)
        stats_output["Korelasyon Matrisi"] = corr

    # Kategorik analiz
    st.subheader("📋 Kategorik Değişken Analizi")
    selected_cats = st.multiselect("Kategorik sütunları seçin:", cat_cols)

    for col in selected_cats:
        st.markdown(f"### 🔹 {col}")
        freq = df[col].value_counts()
        percent = df[col].value_counts(normalize=True) * 100
        freq_table = pd.DataFrame({"Frekans": freq, "Yüzde (%)": percent.round(2)})
        st.dataframe(freq_table)
        stats_output[f"{col} - Frekans"] = freq_table

        fig, ax = plt.subplots()
        freq.plot(kind='bar', ax=ax)
        ax.set_title(f"{col} - Bar Grafiği")
        st.pyplot(fig)

    # PDF çıktısı
    if st.button("📤 PDF Olarak Dışa Aktar"):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Tanımlayıcı İstatistikler Raporu", styles["Heading1"]))

        for title, table_data in stats_output.items():
            elements.append(Paragraph(title, styles["Heading2"]))
            df_data = table_data.reset_index()
            data = [df_data.columns.tolist()] + df_data.values.tolist()
            t = Table(data)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]))
            elements.append(t)

        doc.build(elements)
        st.success("PDF başarıyla oluşturuldu!")
        st.download_button("📥 PDF İndir", buffer.getvalue(), file_name="istatistik_raporu.pdf")

else:
    st.info("Lütfen bir Excel dosyası yükleyin.")
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Sayfa ayarları
st.set_page_config(page_title="Tanımlayıcı İstatistikler", layout="wide")
st.title("📊 Gelişmiş Tanımlayıcı (Betimleyici) İstatistik Uygulaması")

# Renk teması
theme = st.selectbox("🎨 Tema seçin", ["light", "dark", "seaborn", "whitegrid", "ticks"])
sns.set_theme(style=theme)

# Excel yükleme
uploaded_file = st.file_uploader("📂 Excel dosyanızı yükleyin", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("🔍 Veri Önizleme")
    st.dataframe(df.head())

    # Eksik verileri yönet
    st.write("🧩 Eksik Değer Sayıları:")
    st.write(df.isnull().sum())

    fill_method = st.radio("Eksik verilerle nasıl işlem yapılsın?", ["Boş bırak (NaN)", "0 ile doldur", "Satırı sil"])
    if fill_method == "0 ile doldur":
        df = df.fillna(0)
    elif fill_method == "Satırı sil":
        df = df.dropna()

    # Otomatik veri tipi tanıma
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Sayısal analiz
    st.subheader("📈 Sayısal Değişken Analizi")
    selected_nums = st.multiselect("Sayısal sütunları seçin:", numeric_cols)

    stats_output = {}

    if selected_nums:
        stats = df[selected_nums].describe().T
        stats["mod"] = df[selected_nums].mode().iloc[0]
        st.dataframe(stats)
        stats_output["Sayısal İstatistikler"] = stats

        for col in selected_nums:
            st.markdown(f"### 🔸 {col}")
            fig1, ax1 = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax1)
            ax1.set_title(f"{col} - Histogram")
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df[col], ax=ax2)
            ax2.set_title(f"{col} - Boxplot")
            st.pyplot(fig2)

    # Korelasyon Matrisi
    if st.checkbox("📌 Korelasyon matrisini göster"):
        st.subheader("🔗 Korelasyon Matrisi")
        corr = df[numeric_cols].corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr)
        st.pyplot(fig_corr)
        stats_output["Korelasyon Matrisi"] = corr

    # Kategorik analiz
    st.subheader("📋 Kategorik Değişken Analizi")
    selected_cats = st.multiselect("Kategorik sütunları seçin:", cat_cols)

    for col in selected_cats:
        st.markdown(f"### 🔹 {col}")
        freq = df[col].value_counts()
        percent = df[col].value_counts(normalize=True) * 100
        freq_table = pd.DataFrame({"Frekans": freq, "Yüzde (%)": percent.round(2)})
        st.dataframe(freq_table)
        stats_output[f"{col} - Frekans"] = freq_table

        fig, ax = plt.subplots()
        freq.plot(kind='bar', ax=ax)
        ax.set_title(f"{col} - Bar Grafiği")
        st.pyplot(fig)

    # PDF çıktısı
    if st.button("📤 PDF Olarak Dışa Aktar"):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Tanımlayıcı İstatistikler Raporu", styles["Heading1"]))

        for title, table_data in stats_output.items():
            elements.append(Paragraph(title, styles["Heading2"]))
            df_data = table_data.reset_index()
            data = [df_data.columns.tolist()] + df_data.values.tolist()
            t = Table(data)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]))
            elements.append(t)

        doc.build(elements)
        st.success("PDF başarıyla oluşturuldu!")
        st.download_button("📥 PDF İndir", buffer.getvalue(), file_name="istatistik_raporu.pdf")

else:
    st.info("Lütfen bir Excel dosyası yükleyin.")