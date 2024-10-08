class AnalyticsTool:
    def __init__(self, df):
        self.df = df

    def create_sum_order_items_df(self):
        sum_order_items_df = self.df.groupby("product_category_name_english")["order_item_id"].count().reset_index()
        sum_order_items_df.rename(columns={
            "order_item_id": "order_item_count"
        }, inplace=True)
        sum_order_items_df = sum_order_items_df.sort_values(by='order_item_count', ascending=False)

        return sum_order_items_df

    def create_monthly_performance_df(self):
        monthly_performance = self.df.resample('M', on='order_purchase_timestamp').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        monthly_performance.index = monthly_performance.index.strftime('%B')
        monthly_performance = monthly_performance.reset_index()
        monthly_performance.rename(columns={
            "order_id": "order_count",
            "payment_value": "total_revenue"
        }, inplace=True)
        recent_months_performance = monthly_performance.tail(8)

        return recent_months_performance
    
    def create_daily_order_df(self):
        daily_order_df = self.df.resample(rule='D', on='order_purchase_timestamp').agg({
            "order_id": "nunique",
            "payment_value": "sum"
        })
        daily_order_df = daily_order_df.reset_index()
        daily_order_df.rename(columns={
            "order_id": "order_count",
            "payment_value": "total_revenue"
        }, inplace=True)
        
        return daily_order_df
    
    def create_sum_spend_df(self):
        sum_spend_df = self.df.resample(rule='D', on='order_purchase_timestamp').agg({
            "payment_value": "sum"
        })
        sum_spend_df = sum_spend_df.reset_index()
        sum_spend_df.rename(columns={
            "payment_value": "total_spend"
        }, inplace=True)

        return sum_spend_df
      
    def create_city_df(self):
        bycity_df = self.df.groupby("customer_city")['customer_id'].nunique().reset_index()
        bycity_df.rename(columns={
            "customer_id": "customer_count"
        }, inplace=True)
        most_city = bycity_df.loc[bycity_df['customer_count'].idxmax(), 'customer_city']
        bycity_df = bycity_df.sort_values(by='customer_count', ascending=False)

        return bycity_df, most_city

    def create_rfm_df(self):
        rfm_df = self.df.groupby(by="customer_unique_id", as_index=False).agg({
            "order_purchase_timestamp": "max", 
            "order_id": "nunique",
            "payment_value": "sum"
        })
        rfm_df.columns = ["customer_unique_id", "max_order_timestamp", "frequency", "monetary"]
        rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
        recent_date = self.df["order_purchase_timestamp"].dt.date.max()
        rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
        rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
        return rfm_df
    
class BrazilGeospatial:
    def __init__(self, data, plt, mpimg, urllib, st):
        self.data = data
        self.plt = plt
        self.mpimg = mpimg
        self.urllib = urllib
        self.st = st

    def plot(self):
        brazil = self.mpimg.imread(self.urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'),'jpg')
        ax = self.data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", figsize=(10,10), alpha=0.3,s=0.3,c='green')
        self.plt.axis('off')
        self.plt.imshow(brazil, extent=[-73.98283055, -33.8,-33.75116944,5.4])
        self.st.pyplot()
