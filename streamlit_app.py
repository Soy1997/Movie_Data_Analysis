import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Movie Data Analysis Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("mymoviedb.csv", lineterminator='\n')

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
genres = st.sidebar.multiselect("Select Genre", sorted(df['Genre'].dropna().unique()))
years = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), 
                           (int(df['Year'].min()), int(df['Year'].max())))

# Apply filters
filtered_df = df.copy()
if genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(genres)]
filtered_df = filtered_df[(filtered_df['Year'] >= years[0]) & (filtered_df['Year'] <= years[1])]

# Dashboard title
st.title("🎬 Movie Data Analysis Dashboard")

# Show dataset preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

# Show basic info
st.subheader("Dataset Summary")
st.write(f"Total Movies: {filtered_df.shape[0]}")
st.write(filtered_df.describe())

# Genre distribution
st.subheader("Genre Distribution")
fig, ax = plt.subplots()
sns.countplot(y='Genre', data=filtered_df, order=filtered_df['Genre'].value_counts().index, ax=ax)
st.pyplot(fig)

# Ratings over time
st.subheader("Average Rating Over Years")
fig, ax = plt.subplots()
avg_rating_per_year = filtered_df.groupby('Year')['Rating'].mean().reset_index()
sns.lineplot(data=avg_rating_per_year, x='Year', y='Rating', marker='o', ax=ax)
st.pyplot(fig)

# Top rated movies
st.subheader("Top Rated Movies")
top_movies = filtered_df.sort_values(by='Rating', ascending=False).head(10)
st.table(top_movies[['Title', 'Genre', 'Year', 'Rating']])

