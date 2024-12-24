import pandas as pd
import streamlit as st
import preprocesser 

df=pd.read_csv("Data.csv")
print(df.head())

#Title for dashboard
st.title("sales analysis dashboard")

#creating time features
df=preprocesser.fetch_time_features(df)


#side bar for filters

st.sidebar.title("Filters")

#Filters
selected_year=preprocesser.multiselect("Select Year",df["Finantial_year"].unique())
selected_retailer=preprocesser.multiselect("Select Retailer",df["Retailer"].unique())
selected_company=preprocesser.multiselect("Select company",df["Company"].unique())
selected_month=preprocesser.multiselect("Select financial month",df["Finantial_month"].unique())


filtered_df=df[df["Finantial_year"].isin(selected_year)&
                 df["Retailer"].isin(selected_retailer)&
                  df["Company"].isin(selected_company)&
                   df["Finantial_month"].isin(selected_month)]



#KPI - Key performance indicator
#create columns for displaying KPIs
col1,col2,col3,col4 = st.columns(4)

#total sales
with col1:
    st.metric(label="Total Sales",value=f'₹{int(filtered_df["Amount"].sum())}')

#Total margin
with col2:
    st.metric(label="Total Margin",value=f'₹{int(filtered_df["Margin"].sum())}')
#Total Transactions
with col3:
    st.metric(label="Total Transaction",value=len(filtered_df))
#Margin percentage
with col4:
    st.metric(label="Margin Percentage",value=f"{int((filtered_df["Margin"].sum()*100)/(filtered_df["Amount"].sum()))}%")
    
#Visualization to analyze month-on-month sales trends
yearly_sales=(filtered_df[['Finantial_year','Finantial_month','Amount']]
              .groupby(['Finantial_year','Finantial_month'])
              .sum()
              .reset_index()
              .pivot(index="Finantial_month",columns="Finantial_year",values='Amount'))
st.line_chart(yearly_sales,x_label="Finantial_month",y_label="Total Sales")

#visualize retailer count by revenue persentage

col5,col6=st.columns(2)

with col5:
    st.title("Retailer count by revenue %")
    retailer_count=preprocesser.fetch_top_revenue_retailer(filtered_df)
    retailer_count.set_index("percentage revenue",inplace=True)
    st.bar_chart(retailer_count,x_label="percentage revenue",y_label="retailer_count")
with col6:
    st.title("company count by revenue %")
    company_count=preprocesser.fetch_top_revenue_companies(filtered_df)
    company_count.set_index("percentage revenue",inplace=True)
    st.bar_chart(company_count,x_label="percentage revenue",y_label="company_count")  
