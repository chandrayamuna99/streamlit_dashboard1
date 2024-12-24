import pandas as pd
import streamlit as st

#function to create multiselect option in streamlit
def multiselect(title, options_list):
    selected=st.sidebar.multiselect(title,options_list)
    select_all=st.sidebar.checkbox("Select all",value=True,key=title)
    if select_all:
        selected_options=options_list
    else:
        selected_options=selected
    return selected_options

#fetching the date features
def fetch_time_features(df):
    df["Date"]=pd.to_datetime(df["Date"])
    df["Year"]=df["Date"].dt.year
    df["Month"]=df["Date"].dt.month
    df["Day"]=df["Date"].dt.day
    #financial month
    month_dict={4:1,5:2,6:3,7:4,8:5,9:6,10:7,11:8,12:9,1:10,2:11,3:12}
    df["Finantial_month"]=df["Month"].map(month_dict)
    df["Finantial_year"]=df.apply(lambda x: f'{x["Year"]}-{x["Year"]+1}' if x["Month"]>=4 else f'{x["Year"]-1}-{x['Year']}',axis=1)
                                 
    return df

#retailer revenue
def fetch_top_revenue_retailer(df):
    retailer_revenue=df[["Retailer","Amount"]].groupby("Retailer").sum().reset_index().sort_values(by="Amount",ascending=False)
    total_revenue=retailer_revenue["Amount"].sum()
    percentages=[100,90,80,70,60,50,40,30,20,10]
    retail_count=[]
    for i in percentages:
        target_revenue=0.01*i*total_revenue
        loop=1
        while loop<=len(retailer_revenue) and retailer_revenue.iloc[:loop,1].sum()<=target_revenue:
            loop+=1
        retail_count.append(loop)
    retailers=pd.DataFrame(data={"percentage revenue":percentages,"retailer count":retail_count})
    return retailers

#company revenue
def fetch_top_revenue_companies(df):
    company_revenue=df[["Company","Amount"]].groupby("Company").sum().reset_index().sort_values(by="Amount",ascending=False)
    total_revenue=company_revenue["Amount"].sum()
    percentages=[100,90,80,70,60,50,40,30,20,10]
    company_count=[]
    for i in percentages:
        target_revenue=0.01*i*total_revenue
        loop=1
        while loop<=len(company_revenue) and company_revenue.iloc[:loop,1].sum()<=target_revenue:
            loop+=1
        company_count.append(loop)
    companies=pd.DataFrame(data={"percentage revenue":percentages,"company count":company_count})
    return companies
