import streamlit as st
import pandas as pd
import json
import os
#from pprint import pprint
import sqlite3
import base64
import time
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

SQLITE_DB_PATH = "details.db"
sqlite_connection = sqlite3.connect(SQLITE_DB_PATH)
sqlite_cursor = sqlite_connection.cursor() 


Year_select = ''
Quater_select = ''

Type_select = st.sidebar.selectbox(
    'Select the Type:',
    ('','Aggregated_Transaction', 'Aggregated_User', 'Map_Transaction', 'Map_user', 'Top_Transaction', 'Top_user'))

if Type_select == "Aggregated_Transaction":
    Year_select = st.sidebar.selectbox(
        'Select the year:',
        ('','2018', '2019', '2020', '2021', '2022', '2023'))
    if Year_select == '2023':
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2'))
    else :
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2', 'Q3', 'Q4'))

if Type_select == "Aggregated_User":
    Year_select = st.sidebar.selectbox(
        'Select the year:',
        ('','2018', '2019', '2020', '2021', '2022'))
    if Year_select == '2022':
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1','Q2'))
    else :
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2', 'Q3', 'Q4'))
        
if Type_select == "Map_Transaction":
    Year_select = st.sidebar.selectbox(
        'Select the year:',
        ('','2018', '2019', '2020', '2021', '2022', '2023'))
    if Year_select == '2023':
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2'))
    else :
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2', 'Q3', 'Q4'))        
     
if Type_select == "Map_user":
    Year_select = st.sidebar.selectbox(
        'Select the year:',
        ('','2018', '2019', '2020', '2021', '2022', '2023'))
    if Year_select == '2023':
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2'))
    else :
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2', 'Q3', 'Q4')) 

if Type_select == "Top_Transaction":
    Year_select = st.sidebar.selectbox(
        'Select the year:',
        ('','2018', '2019', '2020', '2021', '2022', '2023'))
    if Year_select == '2023':
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2'))
    else :
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2', 'Q3', 'Q4'))        
     
if Type_select == "Top_user":
    Year_select = st.sidebar.selectbox(
        'Select the year:',
        ('','2018', '2019', '2020', '2021', '2022', '2023'))
    if Year_select == '2023':
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2'))
    else :
        Quater_select = st.sidebar.selectbox(
            'Select the Quater:',
            ('','Q1', 'Q2', 'Q3', 'Q4'))

if Quater_select == "":
    Quater_select_val = ''
if Quater_select == "Q1":
    Quater_select_val = 1
if Quater_select == "Q2":
    Quater_select_val = 2
if Quater_select == "Q3":
    Quater_select_val = 3        
if Quater_select == "Q4":
    Quater_select_val = 4

table_name = Type_select
quarter_value = Quater_select_val
year_value = Year_select

if table_name == '':
    table_name_ok = False
else:
    table_name_ok = True

if Quater_select == '':
    Quater_select_ok = False
else:
    Quater_select_ok = True

if Year_select =='':
    Year_select_ok = False
else:
    Year_select_ok = True


def Categories(dataset,type_list,column1,column2):
        Categories_list ={}
        for i in type_list:
            val = {i:dataset[dataset[column1].isin([i])][column2].sum()}
            Categories_list.update(val)
        return Categories_list 

def Top_10_count(dataset,type_list,column1,column2,key_name):
        seperate_list = {}
        for j in type_list:
            state_wise = {j:dataset[dataset[column1].isin([j])][column2].sum()}
            seperate_list.update(state_wise)

        sorted_data = dict(sorted(seperate_list.items(), key=lambda item: item[1], reverse=True)[:10])
        area_val = []
        count_val = []
        for key, value in sorted_data.items():
            #Top_10_area = (f'{key}: {value}')  
            Top_10_area_1 = {key_name:key}
            area_val.append(Top_10_area_1)
            Top_10_area_2 = {"Count":value}
            count_val.append(Top_10_area_2)
        df_1= pd.DataFrame(area_val)
        df_2= pd.DataFrame(count_val)
        result_df = pd.merge(df_1, df_2, left_index=True, right_index=True)
        return(result_df)   

if Year_select_ok and Quater_select_ok and table_name_ok: 
    sql_query = "SELECT * FROM {} WHERE Quater=? AND Year=?".format(table_name)
    year_value = int(year_value)
    q = sqlite_cursor.execute(sql_query,(quarter_value,year_value))
    result = sqlite_cursor.fetchall()
    # print("--------->",result)

    if table_name == "Aggregated_Transaction":
        query_result = pd.DataFrame(result,columns =["State", "Year", "Quater","Transacion_type","Transacion_count","Transacion_amount"])
        Agg_Trans_amount_count = float(query_result["Transacion_amount"].sum())
        Agg_Trans_count = float(query_result["Transacion_count"].sum())
        Agg_Trans_payment_count = float(query_result["Transacion_amount"].mean())
        Agg_Trans_avg = (Agg_Trans_amount_count) // (Agg_Trans_count)
        First = str(Agg_Trans_amount_count)
        Second = str(Agg_Trans_count)
        Third = str(Agg_Trans_payment_count)
        Fourth = str(Agg_Trans_avg)

        Agg_trans_type_list = (query_result["Transacion_type"].unique().tolist())
        Agg_trans_state_list = (query_result["State"].unique().tolist())

        Agg_Trans_category = Categories(dataset=query_result,type_list=Agg_trans_type_list,column1 = "Transacion_type",column2="Transacion_amount")
        Agg_Trans_top_10 = Top_10_count(dataset = query_result,type_list = Agg_trans_state_list,column1="State" ,column2="Transacion_amount" ,key_name = "State")
    

        Transactions = "Transactions:"
        Sub_top1 = "All PhonePe transactions (UPI + Cards + Wallets)"
        Sub_top2 = "Total payment Count"     
        Sub_top3 = "Total payment value" 
        Sub_top4 = "Avg. transaction value"  
        Sub_top5 = "Aggregated Transaction category:"
        Sub_top6 = "Top 10 Aggregated Transaction state wise amount:"
        font_size = 16

        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Transactions}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top1}</span>** : <span style="color: white; font-size: 18px;">{First}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top2}</span>** : <span style="color: white; font-size: 18px;">{Second}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top3}</span>** : <span style="color: white; font-size: 18px;">{Third}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top4}</span>** : <span style="color: white; font-size: 18px;">{Fourth}</span>', unsafe_allow_html=True)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top5}</span>', unsafe_allow_html=True)
        st.dataframe(Agg_Trans_category)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top6}</span>', unsafe_allow_html=True)
        st.dataframe(Agg_Trans_top_10)

    if table_name == "Aggregated_User":
        query_result = pd.DataFrame(result,columns =["State", "Year", "Quater","brand","count","percentage"])
        Agg_user_amount_count = float(query_result["count"].sum())
        First = str(Agg_user_amount_count)

        Agg_user_brand_list = (query_result["brand"].unique().tolist())
        Agg_user_state_list = (query_result["State"].unique().tolist())

        Agg_user_category = Categories(dataset=query_result,type_list=Agg_user_brand_list,column1 = "brand",column2="percentage")
        print(Agg_user_category)
        Agg_user_top_10 = Top_10_count(dataset = query_result,type_list = Agg_user_state_list,column1="State" ,column2="count" ,key_name = "State")
        print(Agg_user_top_10)

        Transactions = "Users:"
        Sub_top1 = "PhonePe Users count"
        Sub_top2 = "Aggregated User category:"
        Sub_top3 = "Top 10 Aggregated User state wise count:"

        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Transactions}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top1}</span>** : <span style="color: white; font-size: 18px;">{First}</span>', unsafe_allow_html=True)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top2}</span>', unsafe_allow_html=True)
        st.dataframe(Agg_user_category)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top3}</span>', unsafe_allow_html=True)
        st.dataframe(Agg_user_top_10)
       
    if table_name == "Map_Transaction":  
        query_result = pd.DataFrame(result,columns =["State", "Year", "Quater","District_name","Transacion_type","Transacion_count","Transacion_amount"]) 
        Map_trans_amount_count = float(query_result["Transacion_amount"].sum())
        Map_trans_count = float(query_result["Transacion_count"].sum())
        Map_trans_payment_count = float(query_result["Transacion_amount"].mean()) 
        Map_trans_avg = (Map_trans_amount_count // Map_trans_count) 
        First = str(Map_trans_amount_count)
        Second = str(Map_trans_count)
        Third = str(Map_trans_payment_count)
        Fourth = str(Map_trans_avg)

        Map_trans_state_list = (query_result["State"].unique().tolist())
        Map_trans_dist_list = (query_result["District_name"].unique().tolist())

        Map_Trans_top_10_state = Top_10_count(dataset = query_result,type_list = Map_trans_state_list,column1="State" ,column2="Transacion_amount" ,key_name = "State")
        print(Map_Trans_top_10_state)
        Map_Trans_top_10_dist = Top_10_count(dataset = query_result,type_list = Map_trans_dist_list,column1="District_name" ,column2="Transacion_amount" ,key_name = "District")
        print(Map_Trans_top_10_dist)

        Transactions = "Transactions:"
        Sub_top1 = "All PhonePe transactions (UPI + Cards + Wallets)"
        Sub_top2 = "Total payment Count"     
        Sub_top3 = "Total payment value" 
        Sub_top4 = "Avg transaction value"    
        Sub_top5 = "Top 10 Map Transaction state wise amount:"
        Sub_top6 = "Top 10 Map Transaction district wise amount:"

        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Transactions}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top1}</span>** : <span style="color: white; font-size: 18px;">{First}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top2}</span>** : <span style="color: white; font-size: 18px;">{Second}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top3}</span>** : <span style="color: white; font-size: 18px;">{Third}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top4}</span>** : <span style="color: white; font-size: 18px;">{Fourth}</span>', unsafe_allow_html=True)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top5}</span>', unsafe_allow_html=True)
        st.dataframe(Map_Trans_top_10_state)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top6}</span>', unsafe_allow_html=True)
        st.dataframe(Map_Trans_top_10_dist)

    if table_name == "Map_user": 
        query_result = pd.DataFrame(result,columns =["State", "Year", "Quater","District_name","registeredUsers","appOpens"])
        Map_user_app_open_count = float(query_result["appOpens"].sum())
        Map_user_reg_users_count = float(query_result["registeredUsers"].sum()) 
        First = str(Map_user_app_open_count)
        Second = str(Map_user_reg_users_count)

        Map_user_state_list = (query_result["State"].unique().tolist())
        Map_user_dist_list = (query_result["District_name"].unique().tolist())

        Map_user_top_10_state = Top_10_count(dataset = query_result,type_list = Map_user_state_list,column1="State" ,column2="registeredUsers" ,key_name = "State")
        print(Map_user_top_10_state)
        Map_user_top_10_dist = Top_10_count(dataset = query_result,type_list = Map_user_dist_list,column1="District_name" ,column2="registeredUsers" ,key_name = "District")
        print(Map_user_top_10_dist)

        Transactions = "Users:"
        Sub_top1 = "PhonePe app openers count"
        Sub_top2 = "PhonePe app registered users count"
        Sub_top3 = "Top 10 State wise Map Transaction Registered users:"
        Sub_top4 = "Top 10 District wise Map Transaction Registered users:"
        


        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Transactions}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top1}</span>** : <span style="color: white; font-size: 18px;">{First}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top2}</span>** : <span style="color: white; font-size: 18px;">{Second}</span>', unsafe_allow_html=True)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top3}</span>', unsafe_allow_html=True)
        st.dataframe(Map_user_top_10_state)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top4}</span>', unsafe_allow_html=True)
        st.dataframe(Map_user_top_10_dist)
        


    if table_name == "Top_Transaction": 
        query_result = pd.DataFrame(result,columns =["State", "Year", "Quater","District_name","Transacion_type","Transacion_count","Transacion_amount"])
        Top_trans_amount_count = float(query_result["Transacion_amount"].sum())
        Top_trans_count = float(query_result["Transacion_count"].sum())
        Top_trans_payment_count = float(query_result["Transacion_amount"].mean()) 
        Top_trans_avg = (Top_trans_amount_count // Top_trans_count) 
        First = str(Top_trans_amount_count)
        Second = str(Top_trans_count)
        Third = str(Top_trans_payment_count)
        Fourth = str(Top_trans_avg) 

        Top_trans_state_list = (query_result["State"].unique().tolist())
        Top_trans_dist_list = (query_result["District_name"].unique().tolist())

        Top_Trans_top_10_state = Top_10_count(dataset = query_result,type_list = Top_trans_state_list,column1="State" ,column2="Transacion_amount" ,key_name = "State")
        print(Top_Trans_top_10_state)
        Top_Trans_top_10_dist = Top_10_count(dataset = query_result,type_list = Top_trans_dist_list,column1="District_name" ,column2="Transacion_amount" ,key_name = "District")
        print(Top_Trans_top_10_dist)

        Transactions = "Transactions:"
        Sub_top1 = "All PhonePe transactions (UPI + Cards + Wallets)"
        Sub_top2 = "Total payment Count"     
        Sub_top3 = "Total payment value" 
        Sub_top4 = "Avg. transaction value"
        Sub_top5 = "Top 10 Top Transaction state wise amount:"
        Sub_top6 = "Top 10 Top Transaction district wise amount:"

        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Transactions}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top1}</span>** : <span style="color: white; font-size: 18px;">{First}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top2}</span>** : <span style="color: white; font-size: 18px;">{Second}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top3}</span>** : <span style="color: white; font-size: 18px;">{Third}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top4}</span>** : <span style="color: white; font-size: 18px;">{Fourth}</span>', unsafe_allow_html=True)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top5}</span>', unsafe_allow_html=True)
        st.dataframe(Top_Trans_top_10_state)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top6}</span>', unsafe_allow_html=True)
        st.dataframe(Top_Trans_top_10_dist)

    if table_name == "Top_user": 
        query_result = pd.DataFrame(result,columns =["State", "Year", "Quater","District_name","registeredUsers","pincode","registeredUsers_1"])
        Top_user_amount_count = float(query_result["registeredUsers"].sum())
        Top_user_count = float(query_result["registeredUsers_1"].sum()) 
        First = str(Top_user_amount_count)
        Second = str(Top_user_count)

        Top_user_state_list = (query_result["State"].unique().tolist())
        Top_user_dist_list = (query_result["District_name"].unique().tolist())

        Top_user_top_10_state = Top_10_count(dataset = query_result,type_list = Top_user_state_list,column1="State" ,column2="registeredUsers" ,key_name = "State")
        print(Top_user_top_10_state)
        Top_user_top_10_dist = Top_10_count(dataset = query_result,type_list = Top_user_dist_list,column1="District_name" ,column2="registeredUsers" ,key_name = "District")
        print(Top_user_top_10_dist)

        Transactions = "Users:"
        Sub_top1 = "PhonePe registered users count"
        Sub_top2 = "PhonePe registered_1 users count"
        Sub_top3 = "Top 10 State wise Top Transaction Registered users:"
        Sub_top4 = "Top 10 District wise Top Transaction Registered users:"  

        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Transactions}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top1}</span>** : <span style="color: white; font-size: 18px;">{First}</span>', unsafe_allow_html=True)
        st.markdown(f'**<span style="color: yellow; font-size: 20px;">{Sub_top2}</span>** : <span style="color: white; font-size: 18px;">{Second}</span>', unsafe_allow_html=True)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top3}</span>', unsafe_allow_html=True)
        st.dataframe(Top_user_top_10_state)
        st.markdown(f'# <span style="color: #74FF33; font-size: 30px;">{Sub_top4}</span>', unsafe_allow_html=True)
        st.dataframe(Top_user_top_10_dist)


if (Quater_select != '') and (year_value != ''):
    print("--------->",query_result)
    #print(Query_result)
    print(query_result["State"])

    pio.renderers.default = "vscode"
    india_states = json.load(open("states_india.geojson",'r'))
    #print(india_states["features"][0].keys())
    replace_dict = {
        'andaman-&-nicobar-islands': 'Andaman & Nicobar Island',
        'andhra-pradesh': 'Andhra Pradesh','arunachal-pradesh':'Arunanchal Pradesh','assam':'Assam','bihar':'Bihar','chandigarh':'Chandigarh','chhattisgarh':'Chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu':'Dadara & Nagar Havelli',
       'delhi':'NCT of Delhi','goa':'Goa','gujarat':'Gujarat','haryana':'Haryana','himachal-pradesh':'Himachal Pradesh','jammu-&-kashmir':'Jammu & Kashmir','jharkhand':'Jharkhand','karnataka':'Karnataka','kerala':'Kerala',
       'ladakh':'Daman & Diu','lakshadweep':'Lakshadweep','madhya-pradesh':'Madhya Pradesh','maharashtra':'Maharashtra','manipur':'Manipur','meghalaya':'Meghalaya','mizoram':'Mizoram','nagaland':'Nagaland','odisha':'Odisha','puducherry':'Puducherry',
       'punjab':'Punjab','rajasthan':'Rajasthan','sikkim':'Sikkim','tamil-nadu':'Tamil Nadu','telangana':'Telangana','tripura':'Tripura','uttar-pradesh':'Uttar Pradesh','uttarakhand':'Uttarakhand','west-bengal':'West Bengal'}
    
    query_result['State'] = query_result['State'].replace(replace_dict)

    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]
    print(state_id_map)
    try:
        query_result["id"] = query_result["State"].apply(lambda x :state_id_map[x])
    except Exception as e:
        print(e)  
   
    
    if table_name == 'Aggregated_Transaction':
        fig = px.choropleth(query_result,locations='id',geojson=india_states,color='Transacion_count',hover_name="State",hover_data=["Transacion_amount"])
        fig.update_geos(fitbounds = "locations",visible = False)    
        st.plotly_chart(fig)
    if table_name == 'Aggregated_User':
        fig = px.choropleth(query_result,locations='id',geojson=india_states,color='percentage',hover_name="State",hover_data=["count"])
        fig.update_geos(fitbounds = "locations",visible = False)    
        st.plotly_chart(fig) 
    if table_name == 'Map_Transaction':
        fig = px.choropleth(query_result,locations='id',geojson=india_states,color='Transacion_count',hover_name="State",hover_data=["Transacion_amount"])
        fig.update_geos(fitbounds = "locations",visible = False)    
        st.plotly_chart(fig)        
    if table_name == 'Map_user':
        fig = px.choropleth(query_result,locations='id',geojson=india_states,color='appOpens',hover_name="State",hover_data=["registeredUsers"])
        fig.update_geos(fitbounds = "locations",visible = False)    
        st.plotly_chart(fig)
    if table_name == 'Top_Transaction':
        fig = px.choropleth(query_result,locations='id',geojson=india_states,color='Transacion_count',hover_name="State",hover_data=["Transacion_amount"])
        fig.update_geos(fitbounds = "locations",visible = False)    
        st.plotly_chart(fig)        
    if table_name == 'Top_user':
        fig = px.choropleth(query_result,locations='id',geojson=india_states,color='registeredUsers_1',hover_name="State",hover_data=["registeredUsers"])
        fig.update_geos(fitbounds = "locations",visible = False)    
        st.plotly_chart(fig)    







        