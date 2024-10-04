import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from function import DataAnalyzer, BrazilMapPlotter

sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Dataset
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("https://raw.githubusercontent.com/nurhadimeilana05/Proyek-Analisis-Data-Dicoding/main/dashboard/all_df.csv")
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv("https://raw.githubusercontent.com/nurhadimeilana05/Proyek-Analisis-Data-Dicoding/main/dashboard/geolocation.csv")
data = geolocation.drop_duplicates(subset='customer_unique_id')

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("https://raw.githubusercontent.com/nurhadimeilana05/Proyek-Analisis-Data-Dicoding/main/dashboard/logo_e-commerce.png"
                 , width=100)
    with col3:
        st.write(' ')

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_order_df = function.create_daily_order_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
city, most_city = function.create_city_df()

# Define your Streamlit app
st.title("E-Commerce Public Dataset")

# Add text or descriptions
st.write("**Hello Everyone! Welcome to Dashboard E-Commerce Public Dataset.**")

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = daily_orders_df["total_revenue"].sum()
    st.markdown(f"Total Revenue: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x=daily_orders_df["order_purchase_timestamp"],
    y=daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#72BF78"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Customer Spend Money
st.subheader("Customer Spend Money")
col1, col2 = st.columns(2)

with col1:
    total_spend = sum_spend_df["total_spend"].sum()
    st.markdown(f"Total Spend: **{total_spend}**")

with col2:
    avg_spend = sum_spend_df["total_spend"].mean()
    st.markdown(f"Average Spend: **{avg_spend}**")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=sum_spend_df,
    x="order_purchase_timestamp",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#72BF78"
)

ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["order_item_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["order_item_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

sns.barplot(x="order_item_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette="mako", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales (Order Item)", fontsize=80)
ax[0].set_title("Best Performing Product", loc="center", fontsize=90)
ax[0].tick_params(axis ='y', labelsize=55)
ax[0].tick_params(axis ='x', labelsize=50)

sns.barplot(x="order_item_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="order_item_count", ascending=True).head(5), palette="mako", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales (Order Item)", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=90)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

# Customer By City
st.subheader("Customer By City")
tab1 = st.tabs(["City"])

with tab1:
    most_city = city.customer_city.value_counts().index[0]
    st.markdown(f"Most Common City: **{most_city}**")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=city.customer_city.value_counts().index,
                y=city.customer_count.values, 
                data=state,
                palette="mako"
                    )

    plt.title("Number customers from City", fontsize=15)
    plt.xlabel("City")
    plt.ylabel("Number of Customers")
    plt.xticks(fontsize=12)
    st.pyplot(fig)
  
st.caption('Copyright (C) Nurhadi Meilana 2024')
