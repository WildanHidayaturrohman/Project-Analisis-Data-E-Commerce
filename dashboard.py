import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membaca file CSV ke dalam dataframe
rfm_df = pd.read_csv("rfm_df.csv")
merged_4_df = pd.read_csv("merged_4_df.csv")
grouped_product_category_review_score = pd.read_csv("grouped_product_category_review_score.csv")
jumlah_pesanan_terlambat_per_state_df = pd.read_csv("jumlah_pesanan_terlambat_per_state_df.csv")
grouped_customer_data = pd.read_csv("grouped_customer_data.csv")
rata_rata_waktu_pengiriman_per_state_df = pd.read_csv("rata_rata_waktu_pengiriman_per_state_df.csv")


# from babel.numbers import format_currency

sns.set(style='dark')

# Judul
st.title("E-commerce Dashboard")

# Sidebar untuk filter

st.sidebar.header("Filter by Product Category")
selected_product = st.sidebar.selectbox("Select Product Category", grouped_product_category_review_score['product_category_name_english'].unique())

# Filter data based on selected product
if selected_product:
    filtered_df = grouped_product_category_review_score[grouped_product_category_review_score['product_category_name_english'] == selected_product]
else:
    filtered_df = grouped_product_category_review_score
# Filter untuk pertanyaan 3 (top/bottom rating)
rating_filter_type = st.sidebar.radio("Pilih Filter Rating (untuk Pertanyaan 3)", ("Top 10", "Bottom 10"))

# Judul visdat
st.title("Visualisasi Data")

# Pertanyaan 1
st.header("Pertanyaan 1: Kategori Pelanggan dalam Setahun Terakhir")

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='Kategori Pelanggan', y='Count', data=grouped_customer_data, ax=ax)  # Replace with your data
plt.title('Kategori Pelanggan dalam Setahun Terakhir')
plt.xlabel('Kategori Pelanggan')
plt.ylabel('Jumlah Pelanggan')
st.pyplot(fig)

# Pertanyaan 2
st.header("Pertanyaan 2: Rata-rata Waktu Pengiriman dan Jumlah Pesanan Terlambat")
# Display 'rata_rata_waktu_pengiriman_per_state_df'
st.subheader("Rata-rata Waktu Pengiriman per State")
st.dataframe(rata_rata_waktu_pengiriman_per_state_df)

# Display 'jumlah_pesanan_terlambat_per_state_df'
st.subheader("Jumlah Pesanan Terlambat per State")
st.dataframe(jumlah_pesanan_terlambat_per_state_df)

# Visualisasi Rata-rata Waktu Pengiriman per State
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='geolocation_state', y='rata_rata_waktu_pengiriman', data=rata_rata_waktu_pengiriman_per_state_df, ax=ax)
plt.title('Rata-rata Waktu Pengiriman per State')
plt.xlabel('State')
plt.ylabel('Rata-rata Waktu Pengiriman (hari)')
plt.xticks(rotation=90)
st.pyplot(fig)

# Visualisasi Jumlah Pesanan Terlambat per State
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='geolocation_state', y='jumlah_pesanan_terlambat', data=jumlah_pesanan_terlambat_per_state_df, ax=ax)
plt.title('Jumlah Pesanan Terlambat per State')
plt.xlabel('State')
plt.ylabel('Jumlah Pesanan Terlambat')
plt.xticks(rotation=90)
st.pyplot(fig)


# Pertanyaan 3
st.header("Pertanyaan 3: Rating Ulasan Produk")

if rating_filter_type == "Top 10":
    top_10_categories = grouped_product_category_review_score.groupby('product_category_name_english')['review_score'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=top_10_categories.index, y=top_10_categories.values, ax=ax)
    plt.title('Kategori Produk dengan Rating Ulasan Tertinggi (Top 10)')
    plt.xlabel('Kategori Produk')
    plt.ylabel('Rata-rata Rating Ulasan')
    plt.xticks(rotation=90)
    st.pyplot(fig)
else:
    bottom_10_categories = grouped_product_category_review_score.groupby('product_category_name_english')['review_score'].mean().sort_values(ascending=True).head(10)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=bottom_10_categories.index, y=bottom_10_categories.values, ax=ax)
    plt.title('Kategori Produk dengan Rating Ulasan Terendah (Bottom 10)')
    plt.xlabel('Kategori Produk')
    plt.ylabel('Rata-rata Rating Ulasan')
    plt.xticks(rotation=90)
    st.pyplot(fig)

st.header("Average Review Score per Product Category")

if not filtered_df.empty:
    avg_review_score = filtered_df.groupby('product_category_name_english')['review_score'].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=avg_review_score.index, y=avg_review_score.values)
    plt.title(f"Average Review Score for {selected_product}")
    plt.xlabel("Product Category")
    plt.ylabel("Average Review Score")
    plt.xticks()
    st.pyplot(fig)
else:
    st.write("No data available for the selected product.")

# pertanyaan 4
st.header("Relationship between Shipping Time and Customer Satisfaction")
correlation = merged_4_df["waktu_pengiriman"].corr(merged_4_df["review_score"])
st.write(f"Korelasi antara waktu pengiriman dan kepuasan pelanggan: {correlation:.2f}")

plt.figure(figsize=(8, 6))
sns.scatterplot(x="waktu_pengiriman", y="review_score", data=merged_4_df)
plt.title('Hubungan antara Waktu Pengiriman dan Kepuasan Pelanggan')
plt.xlabel('Waktu Pengiriman (hari)')
plt.ylabel('Rating Ulasan')
st.pyplot(plt)

# RFM analysis
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
sns.barplot(
    x="Recency",
    y="customer_id",
    data=rfm_df.sort_values(by="Recency", ascending=True).head(5),
    palette=colors,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis="x", labelsize=15)

sns.barplot(
    x="Frequency",
    y="customer_id",
    data=rfm_df.sort_values(by="Frequency", ascending=False).head(5),
    palette=colors,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis="x", labelsize=15)

sns.barplot(
    x="Monetary",
    y="customer_id",
    data=rfm_df.sort_values(by="Monetary", ascending=False).head(5),
    palette=colors,
    ax=ax[2]
)
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis="x", labelsize=15)

plt.suptitle("Best Customer Based on RFM Parameters (customer_id)", fontsize=20)

# Tambahan
st.header("RFM Analysis - Descriptive Statistics")
st.dataframe(rfm_df.describe())

# RFM distributions
st.header("RFM Distributions")
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
sns.boxplot(y='Recency', data=rfm_df, ax=ax[0])
ax[0].set_title('Recency Distribution')
sns.boxplot(y='Frequency', data=rfm_df, ax=ax[1])
ax[1].set_title('Frequency Distribution')
sns.boxplot(y='Monetary', data=rfm_df, ax=ax[2])
ax[2].set_title('Monetary Distribution')
plt.tight_layout()
st.pyplot(fig)

st.header("Kesimpulan Analysis RFM")
st.write("""
### 1. Recency
- Rata rata pelanggan bertransaksi adalah 290 hari yang lalu
- Ada pelanggan yang baru saja bertransaksi (0 hari), dan ada yang tidak bertransaksi hingga 772 hari
- 50% pelanggan terakhir bertransaksi dalam 271 hari
### 2. Frequency
- Semua pelanggan memiliki frekuensi transaksi = 1, yang berarti setiap pelanggan hanya melakukan satu transaksi
- Ini menunjukkan bahwa dataset ini kemungkinan besar berasal dari bisnis dengan model transaksi sekali beli.
### 3. Monetary
- Rata-rata pelanggan membelanjakan $160.99

- Ada pelanggan yang hanya membelanjakan $9.59

- Ada juga pelanggan yang menghabiskan hingga $13,664.08


- 50% pelanggan membelanjakan kurang dari $105.29

- 75% kurang dari $176.97, menunjukkan bahwa sebagian besar transaksi bernilai kecil, tetapi ada beberapa pelanggan dengan transaksi besar

#### Insight
- Bisnis ini memiliki banyak pelanggan sekali beli, yang berarti perlu strategi retensi pelanggan, seperti program loyalitas atau promosi untuk mendorong repeat purchase
- Beberapa pelanggan memiliki nilai pembelian yang sangat tinggi, sehingga bisnis bisa menerapkan strategi VIP atau layanan premium untuk mempertahankan mereka
- Recency cukup tinggi, yang menunjukkan bahwa banyak pelanggan tidak kembali dalam waktu lama. Kampanye re-engagement bisa membantu menarik mereka kembali
""")

st.header("Kesimpulan Pertanyaan 1 sampai 4")
st.write("""
- Tidak adanya customer yang melakukan pembelian lebih dari 1 kali merupakan situasi yang sangat genting. Ini bisa memiliki arti bahwa hampir semua customer yang berbelanja tidak puas akan pelayanan ataupun barang yang dipesan
- Salah satu faktor terbesar yang mengakibatkan tidak adanya customer yang melakukan pembelian lebih dari 2 kali adalah waktu pengiriman yang cukup lama. Bahkan dari semua kota yang ada, sebagian besar kota memiliki aaktu pengiriman yang jaauh lebih lama dibanding rata-rata kecepatan waktu pengiriman. Keterlambatan yang terjadi pula merupakan masalah besar dan menjadi alasan utama dari kurang baiknya pelayanan yang mengakibatkan masalah pada point 1. Bahkan jumlah keterlambatan yang ada pula masih sangat banyak. Ini pasti menjadi keresahan customer.
- Dari review dan review score yang diberikan pula, masih banyak produk yang memiliki score rendah. Ini bisa jadi karena kurangnya kualitas produk atau kurangnya pelayanan dari seller.
- Korelasi antara ecepatan waktu pengiriman terhadap kepuasan customers pula menunjukkan angka -0,31. Ini merupakan nilai yang cukup besar, ini berarti bahwa salah satu faktor utama kepuasan pelanggan adalah lamanya proses pengiriman.
- Langkah yang bisa diambil untuk menyelesaikan masalah ini adalah dengan memberikan rekomendasi produk-produk yang serupa atau sejenis dengan produk yang telah dibeli customer lewat platform, email atau pesan, mempercepat dan mengefisiensikan waktu pengiriman serta memperbaiki kualitas produk dan kualitas pelayanan lain.
""")