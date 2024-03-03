pip install matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_customer_df(cust_df):
    cust_count = cust_df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False)
    cust_count_df = cust_count.reset_index().rename(columns={"customer_id": "customer_count"})
    return cust_count_df

def create_payment_df(payment_df):
    payment_count = payment_df.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False)
    payment_count_df = payment_count.reset_index().rename(columns={"order_id": "order_count"})
    return payment_count_df

def create_review_df(review_df):
    review_count = review_df.groupby(by="review_score").review_id.nunique().sort_values(ascending=False)
    review_count_df = review_count.reset_index().rename(columns={"review_id": "review_count"})
    return review_count_df

def create_payview_df(main_df):
    payview_df = main_df.groupby(by=["payment_type"]).agg({
        "order_id": "nunique",
        "review_score": "mean"
    }).reset_index().rename(columns={"order_id": "order_count"})
    return payview_df


all_df = pd.read_csv("all_data.csv")

datetime_columns = ["review_creation_date", "review_answer_timestamp"]
all_df.sort_values(by="review_creation_date", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["review_creation_date"].min()
max_date = all_df["review_creation_date"].max()
 
with st.sidebar:
    st.image("https://github.com/anggiealnrn27/brazilian_Ecommerce/raw/main/1_cxwDFbsfKaPQGd4P5fsPUQ.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["review_creation_date"] >= str(start_date)) & 
                (all_df["review_creation_date"] <= str(end_date))]

data_customer_df = create_customer_df(main_df)
data_payment_df = create_payment_df(main_df)
data_review_df = create_review_df(main_df)
data_payview_df = create_payview_df(main_df)

st.header('Brazilian E-Commerce Public Activity Report :computer:')

cust_count_df = create_customer_df(main_df)
st.subheader('5 Cities With The Most Customers')
col = st.columns(1)
most_cust = cust_count_df.head(5)
max_cust = most_cust["customer_count"].max()
col[0].metric("Max Customers", f"{max_cust}")
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('lightgray')
most_cust.plot(kind='bar', x='customer_city', y='customer_count', color='darkblue', ax=ax)
plt.xlabel('City', fontsize=14)
plt.ylabel('Number of Customers', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
st.pyplot(fig)

payment_count_df = create_payment_df(main_df)
st.subheader('Payment Type Distribution')
fig, ax = plt.subplots(figsize=(8, 8))
fig.patch.set_facecolor("lightgray")
colors = ['blue', 'green', 'yellow', 'brown', 'purple']
ax.pie(payment_count_df['order_count'], labels=payment_count_df['payment_type'], autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Payment Type Used by The Customer', fontsize=17, loc='center')
st.pyplot(fig)

review_count_df = create_review_df(main_df)
review_count_df.set_index("review_score", inplace = True)
review_count_df = review_count_df.reindex(index=range(5, 0, -1))
st.subheader('Number of Ratings from Customers')
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('lightgray')
review_count_df.plot(kind="barh", color = "darkblue", ax=ax)
plt.title('Number of Ratings from Customers', fontsize=17)
plt.xlabel('Total', fontsize=14)
plt.ylabel('Rate', fontsize=14)
st.pyplot(fig)

payview_df = create_payview_df(main_df)
st.subheader('Review Score Based on Payment Type')
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('lightgray')
sns.barplot(x="review_score", y="payment_type", data=payview_df, color='darkblue')
plt.title('Review Score Based on Payment Type', fontsize=17)
plt.xlabel('Review Score', fontsize=14)
plt.ylabel('Payment Type', fontsize=14)
st.pyplot(fig)
