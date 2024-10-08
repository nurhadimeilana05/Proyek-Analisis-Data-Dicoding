import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from function import AnalyticsTool, BrazilGeospatial

sns.set(style='dark')

# Dataset
datetime_cols = [
    "order_approved_at", 
    "order_delivered_carrier_date", 
    "order_delivered_customer_date", 
    "order_estimated_delivery_date", 
    "order_purchase_timestamp", 
    "shipping_limit_date"
]
all_df = pd.read_csv("https://raw.githubusercontent.com/nurhadimeilana05/Proyek-Analisis-Data-Dicoding/main/dashboard/all_df.csv")
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(drop=True, inplace=True) 

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
        st.image(
            "https://raw.githubusercontent.com/nurhadimeilana05/Proyek-Analisis-Data-Dicoding/main/dashboard/logo_e-commerce.png",
            width=100
        )
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
main_df = all_df[
    (all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
    (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

function = AnalyticsTool(main_df)
map_plot = BrazilGeospatial(data, plt, mpimg, urllib, st)

sum_order_items_df = function.create_sum_order_items_df()
recent_months_performance = function.create_monthly_performance_df()
daily_order_df = function.create_daily_order_df()
sum_spend_df = function.create_sum_spend_df()
bycity_df, most_city = function.create_city_df()
rfm_df = function.create_rfm_df()

st.title("E-Commerce Public Dataset")
st.write("**Hello Everyone! Welcome to Dashboard E-Commerce Public Dataset.**")

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["order_item_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["order_item_count"].mean()
    st.markdown(f"Average Items: **{avg_items:.2f}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(50, 25))

colors = ["#72BF78", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Best Performing Product
sns.barplot(
    x="order_item_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.head(5), 
    palette=colors, 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales (Order Item)", fontsize=80)
ax[0].set_title("Best Performing Product", loc="center", fontsize=90)
ax[0].tick_params(axis='y', labelsize=55)
ax[0].tick_params(axis='x', labelsize=50)

# Worst Performing Product
sns.barplot(
    x="order_item_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.sort_values(by="order_item_count", ascending=True).head(5), 
    palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales (Order Item)", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=90)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig)

# Number of Order in Recent Month
st.subheader("Number of Orders in Recent Months")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x="order_purchase_timestamp",
    y="order_count",
    data=recent_months_performance,
    marker="o",
    linewidth=2,
    label='Number of Orders',
    color="#72BF78",
    ax=ax
)

ax.set_ylim(bottom=0)
ax.set_title("Number of Orders in Recent Months (2018)", loc="center", fontsize=20)
ax.set_ylabel("Number of Orders", fontsize=12)
ax.set_xlabel("Month", fontsize=12)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

# Revenue in Recent Months
st.subheader("Revenue in Recent Months")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x="order_purchase_timestamp",
    y="total_revenue",
    data=recent_months_performance,
    marker="o",
    linewidth=2,
    label='Revenue',
    color="#72BF78",
    ax=ax
)

ax.set_ylim(bottom=0)
ax.set_title("Revenue in Recent Months (2018)", loc="center", fontsize=20)
ax.set_ylabel("Revenue", fontsize=12)
ax.set_xlabel("Month", fontsize=12)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
    total_order = daily_order_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = daily_order_df["total_revenue"].sum()
    st.markdown(f"Total Revenue: **{total_revenue}**")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    x="order_purchase_timestamp",
    y="order_count",
    data=daily_order_df,
    marker="o",
    linewidth=2,
    color="#72BF78",
    ax=ax
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
    st.markdown(f"Average Spend: **{avg_spend:.2f}**")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=sum_spend_df,
    x="order_purchase_timestamp",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#72BF78",
    ax=ax
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Customer By City
st.subheader("Customer By City")
tab1, tab2 = st.tabs(["City", "Map"])

with tab1:
    most_city_df = most_city
    st.markdown(f"Most Common City: **{most_city_df}**")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#72BF78"] + ["#D3D3D3"] * 4  
    
    sns.barplot(
        x="customer_city",
        y="customer_count",
        data=bycity_df.head(5),
        palette=colors,
        ax=ax
    )

    ax.set_title("Number of Customers by City", fontsize=20)
    ax.set_xlabel("City")
    ax.set_ylabel("Number of Customers")
    ax.tick_params(axis='x', rotation=45, labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    st.pyplot(fig)

with tab2:
    map_plot.plot()
    
# RFM Analysis
st.subheader("Best Customer Based on RFM Parameters")

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))

colors = ["#72BF78"] * 5

# By Recency
sns.barplot(
    y="recency", 
    x="customer_unique_id", 
    data=rfm_df.sort_values(by="recency", ascending=True).head(5), 
    palette=colors, 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer Unique ID", fontsize=30)
ax[0].set_title("By Recency (days)", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35, rotation=90)

# By Frequency
sns.barplot(
    y="frequency", 
    x="customer_unique_id", 
    data=rfm_df.sort_values(by="frequency", ascending=False).head(5), 
    palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer Unique ID", fontsize=30)
ax[1].set_title("By Frequency", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35, rotation=90)

# By Monetary
sns.barplot(
    y="monetary", 
    x="customer_unique_id", 
    data=rfm_df.sort_values(by="monetary", ascending=False).head(5), 
    palette=colors, 
    ax=ax[2]
)
ax[2].set_ylabel(None)
ax[2].set_xlabel("Customer Unique ID", fontsize=30)
ax[2].set_title("By Monetary", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35, rotation=90)

st.pyplot(fig)

st.caption('Copyright (C) Nurhadi Meilana 2024')
