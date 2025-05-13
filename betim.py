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

# Tema seçimi
theme = st.selectbox("🎨 Tema seçin", ["darkgrid", "whitegrid", "ticks", "dark", "white"])
sns.set_theme(style=theme)

# Excel dosyası yükleme
uploaded_file = st.file_uploader("📂 Excel dosyanızı yükleyin", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("🔍 Veri Önizleme")
    st.dataframe(df.head())

    st.write("🧩 Eksik Değer Sayıları:")
    st.write(df.isnull().sum())

    fill_method = st.radio("Eksik verilerle nasıl işlem yapılsın?", ["Boş bırak (NaN)", "0 ile doldur", "Satırı sil"])
    if fill_method == "0 ile doldur":
        df = df.fillna(0)
    elif fill_method == "Satırı sil":
        df = df.dropna()

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    st.subheader("📈 Sayısal Değişken Analizi")
    selected_nums = st.multiselect("Sayısal sütunları seçin:", numeric_cols)

    stats_output = {}
    charts_output = {}

    if selected_nums:
        stats = df[selected_nums].describe().T
        modes = [df[col].mode().iloc[0] if not df[col].mode().empty else np.nan for col in selected_nums]
        stats["mod"] = modes
        st.dataframe(stats)
        stats_output["Sayısal İstatistikler"] = stats

        st.subheader("📊 Sayısal Değişken Grafikleri (2'li Grid)")

        for i in range(0, len(selected_nums), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(selected_nums):
                    col = selected_nums[i + j]

                    # Histogram
                    fig1, ax1 = plt.subplots(figsize=(5, 3))
                    sns.histplot(df[col], kde=True, ax=ax1)
                    ax1.set_title(f"{col} - Histogram")
                    cols[j].pyplot(fig1)

                    buf1 = BytesIO()
                    fig1.savefig(buf1, format="png")
                    cols[j].download_button(
                        label=f"⬇️ {col} Histogram İndir",
                        data=buf1.getvalue(),
                        file_name=f"{col}_histogram.png",
                        mime="image/png"
                    )

                    # Boxplot
                    fig2, ax2 = plt.subplots(figsize=(5, 3))
                    sns.boxplot(x=df[col], ax=ax2)
                    ax2.set_title(f"{col} - Boxplot")
                    cols[j].pyplot(fig2)

                    buf2 = BytesIO()
                    fig2.savefig(buf2, format="png")
                    cols[j].download_button(
                        label=f"⬇️ {col} Boxplot İndir",
                        data=buf2.getvalue(),
                        file_name=f"{col}_boxplot.png",
                        mime="image/png"
                    )

                    plt.close(fig1)
                    plt.close(fig2)

    if st.checkbox("📌 Korelasyon matrisini göster"):
        st.subheader("🔗 Korelasyon Matrisi")
        corr = df[numeric_cols].corr()
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr)
        st.pyplot(fig_corr)
        charts_output["Korelasyon Matrisi"] = fig_corr
        stats_output["Korelasyon Matrisi"] = corr

        buf_corr = BytesIO()
        fig_corr.savefig(buf_corr, format="png")
        st.download_button(
            label="⬇️ Korelasyon Matrisi İndir",
            data=buf_corr.getvalue(),
            file_name="korelasyon_matrisi.png",
            mime="image/png"
        )
        plt.close(fig_corr)

    # Kategorik analiz
    st.subheader("📋 Kategorik Değişken Analizi")
    selected_cats = st.multiselect("Kategorik sütunları seçin:", cat_cols)

    if selected_cats:
        st.markdown("### 🔹 Frekans Tabloları ve Bar Grafikler (2'li Grid Görünüm)")
        for i in range(0, len(selected_cats), 2):
            cols_row = st.columns(2)

            for j in range(2):
                if i + j < len(selected_cats):
                    col_name = selected_cats[i + j]
                    freq = df[col_name].value_counts()
                    percent = df[col_name].value_counts(normalize=True) * 100
                    freq_table = pd.DataFrame({
                        "Frekans": freq,
                        "Yüzde (%)": percent.round(2)
                    })

                    with cols_row[j]:
                        st.markdown(f"**🔹 {col_name}**")
                        st.dataframe(freq_table)
                        stats_output[f"{col_name} - Frekans"] = freq_table

                        fig, ax = plt.subplots(figsize=(5, 3))
                        freq.plot(kind='bar', ax=ax)
                        ax.set_title(f"{col_name} - Bar Grafiği")
                        st.pyplot(fig)

                        buf = BytesIO()
                        fig.savefig(buf, format="png")
                        st.download_button(
                            label=f"⬇️ {col_name} Bar Grafiği İndir",
                            data=buf.getvalue(),
                            file_name=f"{col_name}_bar.png",
                            mime="image/png"
                        )
                        plt.close(fig)

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
        st.success("✅ PDF başarıyla oluşturuldu!")
        st.download_button("📥 PDF İndir", buffer.getvalue(), file_name="istatistik_raporu.pdf")

else:
    st.info("Lütfen bir Excel dosyası yükleyin.")
