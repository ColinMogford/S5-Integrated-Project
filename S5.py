# Import Libraries
import pandas as pd
import numpy as np
import math as mt
import streamlit as st
import plotly.express as px

# Read dataset
df = pd.read_csv('games.csv')

# Replace column names with lowercase versions
df.columns = map(str.lower, df.columns)

# Add total_sales column
df['total_sales'] = df['eu_sales'] + df['na_sales'] + df['jp_sales'] + df['other_sales']
# Check if total_sales column computed correctly
df.head()

# Address TBDs in user_score
df['user_score'] = df['user_score'].replace('tbd',-1)
# Change data type to float
df['user_score'] = df['user_score'].astype('float')

# Calculate mean user_score for filling null values
score_sum = 0
score_count = 0
for x in df['user_score']:
    if x >= 0:
        score_sum += x
        score_count += 1
score_mean = score_sum/score_count

# Remove small game row per analysis above
df.drop(index=14244,inplace=True)
# Replace name and genre per analysis above
df['name'] = df['name'].fillna('Popular Game')
df['genre'] = df['genre'].fillna('N/A')

# Calculate fill values for null data
year_median = df.groupby('name')['year_of_release'].median().median() # Group data frame by name to avoid skewing the years for duplicate games on different platforms
critic_score_median = df.groupby('name')['critic_score'].median().median() # Group data frame by name to avoid skewing the scores for duplicate games on different platforms

# Fill null values in columns
df['year_of_release'] = df['year_of_release'].fillna(year_median)
df['user_score'] = df['user_score'].fillna(score_mean).replace(-1,score_mean) # Also replacing negative 1 placeholder value for "tbd" in user_score
df['critic_score'] = df['critic_score'].fillna(critic_score_median)
df['rating'] = df['rating'].fillna('RP') # rating column already contains values "RP" for "ratings pending" that we can use for null values in rating column

# Convert data types
df['year_of_release'] = df['year_of_release'].convert_dtypes('int64')

# Check how many games were released in different years
st.header('Games per Year')
fig = px.histogram(
    x = df['year_of_release']
)
st.write(fig)