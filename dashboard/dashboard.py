import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load data from CSV file
all_df = pd.read_csv("all_data.csv")

# Set the title of the dashboard
st.title("Bike Rental Dashboard")

# Display the data in a table
st.subheader("Data Overview")
st.write(all_df)

# Display summary statistics
st.subheader("Summary Statistics")
st.write(all_df.describe())

# Create a line chart for bike rentals over time
st.subheader("Bike Rentals Over Time")
all_df['instant'] = pd.to_datetime(all_df['dteday_x'])  # Convert to datetime
plt.figure(figsize=(10, 5))
plt.plot(all_df['instant'], all_df['cnt_x'], label='Total Rentals', color='blue')
plt.title('Total Bike Rentals Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Rentals')
plt.xticks(rotation=45)
plt.legend()
st.pyplot(plt)

# Create a bar chart for rentals by season
st.subheader("Bike Rentals by Season")
season_counts = all_df['season_x'].value_counts().sort_index()
plt.figure(figsize=(10, 5))
season_counts.plot(kind='bar', color='orange')
plt.title('Total Bike Rentals by Season')
plt.xlabel('Season')
plt.ylabel('Number of Rentals')
st.pyplot(plt)

# Create a histogram for temperature distribution
st.subheader("Temperature Distribution")
plt.figure(figsize=(10, 5))
plt.hist(all_df['temp_x'], bins=20, color='green', alpha=0.7)
plt.title('Temperature Distribution')
plt.xlabel('Temperature')
plt.ylabel('Frequency')
st.pyplot(plt)

# Add a sidebar for user input (optional)
st.sidebar.header("User Input Features")
selected_season = st.sidebar.selectbox("Select Season", options=all_df['season_x'].unique())

# Filter data based on user input
filtered_data = all_df[all_df['season_x'] == selected_season]
st.subheader(f"Filtered Data for Season {selected_season}")
st.write(filtered_data)

# Melakukan RFM Analysis
all_df['dteday_x'] = pd.to_datetime(all_df['dteday_x'])
all_df['recency'] = (all_df['dteday_x'].max() - all_df['dteday_x']).dt.days
all_df['frequency'] = all_df.groupby('registered_x')['cnt_x'].transform('count')
all_df['monetary_value'] = all_df['cnt_x'] * all_df['temp_x']  # Contoh penghitungan nilai moneter berdasarkan jumlah rental dan suhu

# Membuat skor RFM
def rfm_score(row):
    recency_score = 10000 / (row['recency'] + 1)
    frequency_score = row['frequency'] * 10
    monetary_value_score = row['monetary_value'] * 10
    return recency_score + frequency_score + monetary_value_score

all_df['rfm_score'] = all_df.apply(rfm_score, axis=1)

# Contoh membuat skor RFM
def rfm_score(row):
    recency_score = 10000 / (row['recency'] + 1)
    frequency_score = row['frequency'] * 10
    monetary_value_score = row['monetary_value'] * 10
    return recency_score + frequency_score + monetary_value_score

all_df['rfm_score'] = all_df.apply(rfm_score, axis=1)

# Pilih kriteria pembagian cluster
clusters = {
    'Low': all_df[all_df['rfm_score'] < 5000],
    'Medium': all_df[(all_df['rfm_score'] >= 5000) & (all_df['rfm_score'] < 10000)],
    'High': all_df[all_df['rfm_score'] >= 10000]
}

st.title("Dashboard Analisis RFM dan Clustering")

# Tampilan data dasar
st.subheader("Data Dasar")
st.write(all_df)

# Tampilan hasil RFM Analysis
st.subheader("Hasil RFM Analysis")
st.write(all_df[['recency', 'frequency', 'monetary_value', 'rfm_score']])