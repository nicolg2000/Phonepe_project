import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json


connection = mysql.connector.connect(host="localhost", user="root", password="12345", database="phonepay_data")
mycursor = connection.cursor()

#aggregated_insurance df

mycursor.execute("select * from aggregated_insurance")
#connection.commit()
table7=mycursor.fetchall()

Aggregated_insurance=pd.DataFrame(table7,columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))


#aggregated_transaction df

mycursor.execute("select * from aggregated_transaction")
#connection.commit()
table1=mycursor.fetchall()

Aggre_transaction=pd.DataFrame(table1,columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))


#aggregated_user df

mycursor.execute("select * from aggregated_user")
#connection.commit()
table2=mycursor.fetchall()

aggregated_user=pd.DataFrame(table2,columns=("States", "Years", "Quarter", "Brands",
                                               "Transaction_count", "Percentage"))


#map_insurnce_df

mycursor.execute("select * from map_insurance")
#connection.commit()
table8=mycursor.fetchall()

map_insurance=pd.DataFrame(table8,columns=("States", "Years", "Quarter", "Districts",
                                               "Transaction_count", "Transaction_amount"))



#map_transaction df
mycursor.execute("select * from map_transaction")
#connection.commit()
table3=mycursor.fetchall()


map_transaction=pd.DataFrame(table3,columns=("States", "Years", "Quarter", "Districts",
                                               "Transaction_count", "Transaction_amount"))

#map_user df

mycursor.execute("select * from map_user")
#connection.commit()
table4=mycursor.fetchall()

map_user=pd.DataFrame(table4,columns=("States", "Years", "Quarter", "Districts",
                                               "RegisteredUsers", "AppOpens"))


#top_insurance df

mycursor.execute("select * from top_insurance")
#connection.commit()
table9=mycursor.fetchall()

top_insurance=pd.DataFrame(table9,columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))


#top_transaction df

mycursor.execute("select * from top_transaction")
#connection.commit()
table5=mycursor.fetchall()

top_transaction=pd.DataFrame(table5,columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_user df

mycursor.execute("select * from top_user")
#connection.commit()
table6=mycursor.fetchall()

top_user=pd.DataFrame(table6,columns=("States", "Years", "Quarter", "Pincodes",
                                               "RegisteredUsers"))



def Transaction_amount_count_Y(df, year):
    tacy=df[df['Years'] == year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)
        
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)

    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
        
    states_name.sort()
    col1,col2 = st.columns(2)
    with col1:
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
     
    with col2: 
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
    return tacy


def Transaction_amount_count_Y_Q(df, quarter):
    tacy=df[df['Quarter'] == quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)
        st.plotly_chart(fig_count)
    
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)

    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
        
    states_name.sort()
    
    col1,col2 = st.columns(2)
    with col1:
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name="States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
        
        
    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name="States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600, width=600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
        
    return tacy
        
        
def Aggre_tran_transaction_type(df, state):

    tacy=df[df['States'] == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width=600, title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)   


#aggre user analysis 1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)


    fig_bar_1= px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.haline_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy


#aggre user analysis 2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_2= px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence=px.colors.sequential.Magenta, hover_name="Brands")
    st.plotly_chart(fig_bar_2)
    
    return aguyq

#aggre user plot 3
def Aggre_user_plot_3(df, state):
    auyqs=df[df["States"] == state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1=px.line(auyqs, x= "Brands", y="Transaction_count", hover_data="Percentage",
                    title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width=1000, markers=True)
    st.plotly_chart(fig_line_1)
    

#map insurance district
def Map_insur_District(df, state):

    tacy=df[df['States'] == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg, x="Transaction_amount", y="Districts", orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2=px.bar(tacyg, x="Transaction_count", y="Districts", orientation="h",height=600,
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


#map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)

    muyg= muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg, x= "States", y=["RegisteredUsers","AppOpens"],
                    title=f"{year} REGISTERED USER, APPOPENS", width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)
    
    return muy

#map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg= muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg, x= "States", y=["RegisteredUsers","AppOpens"],
                    title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USER, APPOPENS", width=1000, height=800, markers=True,
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    
    return muyq

#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop=True, inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x= "RegisteredUsers", y= "Districts", orientation="h",
                                title= f"{states.upper()} REGISTERED USER", height=800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts", orientation="h",
                                title= f"{states.upper()} APPOPENS", height=800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)
        
        
#top_insur_plot_1
def top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount",hover_data="Pincodes",
                                    title= "TRANSACTION AMOUNT", height=650, width=600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)
    
    with col2:
        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count",hover_data="Pincodes",
                                    title= "TRANSACTION COUNT", height=650, width=600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)
        
        
def top_user_plot_1(df, year):
    tuy= df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)


    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)


    fig_top_plot_1=px.bar(tuyg, x="States", y="RegisteredUsers", color="Quarter",width=1000,
                        height=800, color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)
    
    return tuy


#top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2= px.bar(tuys, x="Quarter", y="RegisteredUsers",
                        title="REGISTERED USER, PINCODES, QUARTER",
                        width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)
    
    
#transaction amount query
def top_chart_transaction_amount(table_name):
    connection = mysql.connector.connect(host="localhost", user="root", password="12345", database="phonepay_data")
    mycursor = connection.cursor()
    #plot1
    query1 = f'''SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount DESC
                LIMIT 10'''
                
    mycursor.execute(query1)
    Table_1 = mycursor.fetchall()
    connection.commit()

    df_1 = pd.DataFrame(Table_1, columns=("States", "Transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="States", y="Transaction_amount", title="TOP 10 TRANSACTION AMOUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)
        st.plotly_chart(fig_amount)


    #plot2
    query2 = f'''SELECT States, SUM(Transaction_amount) AS Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount
                LIMIT 10'''
                
    mycursor.execute(query2)
    Table_2 = mycursor.fetchall()
    connection.commit()

    df_2 = pd.DataFrame(Table_2, columns=("States", "Transaction_amount"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States", y="Transaction_amount", title="LAST 10 TRANSACTION AMOUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650, width=600)
        st.plotly_chart(fig_amount_2)



    #plot3
    query3 = f'''SELECT States, AVG(Transaction_amount) AS Transaction_amount
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_amount'''
                
    mycursor.execute(query3)
    Table_3 = mycursor.fetchall()
    connection.commit()

    df_3 = pd.DataFrame(Table_3, columns=("States", "Transaction_amount"))

    fig_amount_3 = px.bar(df_3, y="States", x="Transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT",hover_name="States",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=800, width=1000)
    st.plotly_chart(fig_amount_3)

  
  
  #transaction count query
def top_chart_transaction_count(table_name):
    connection = mysql.connector.connect(host="localhost", user="root", password="12345", database="phonepay_data")
    mycursor = connection.cursor()
    #plot1
    query1 = f'''SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count DESC
                LIMIT 10'''
                
    mycursor.execute(query1)
    Table_1 = mycursor.fetchall()
    connection.commit()

    df_1 = pd.DataFrame(Table_1, columns=("States", "Transaction_count"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="States", y="Transaction_count", title="TOP 10 TRANSACTION COUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)
        st.plotly_chart(fig_amount)


    #plot2
    query2 = f'''SELECT States, SUM(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count
                LIMIT 10'''
                
    mycursor.execute(query2)
    Table_2 = mycursor.fetchall()
    connection.commit()

    df_2 = pd.DataFrame(Table_2, columns=("States", "Transaction_count"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="States", y="Transaction_count", title="LAST 10 TRANSACTION COUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650, width=600)
        st.plotly_chart(fig_amount_2)



    #plot3
    query3 = f'''SELECT States, AVG(Transaction_count) AS Transaction_count
                FROM {table_name}
                GROUP BY States
                ORDER BY Transaction_count'''
                
    mycursor.execute(query3)
    Table_3 = mycursor.fetchall()
    connection.commit()

    df_3 = pd.DataFrame(Table_3, columns=("States", "Transaction_count"))

    fig_amount_3 = px.bar(df_3, y="States", x="Transaction_count", title="AVERAGE OF TRANSACTION COUNT",hover_name="States",orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=800, width=1000)
    st.plotly_chart(fig_amount_3)
    
    
#top char registered user
def top_chart_registered_user(table_name,state):
    connection = mysql.connector.connect(host="localhost", user="root", password="12345", database="phonepay_data")
    mycursor = connection.cursor()

    query1 = f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers
                    FROM {table_name}
                    WHERE States= '{state}'
                    GROUP BY Districts
                    ORDER BY RegisteredUsers DESC
                    LIMIT 10;'''
                
    mycursor.execute(query1)
    Table_1 = mycursor.fetchall()
    connection.commit()

    df_1 = pd.DataFrame(Table_1, columns=("Districts","RegisteredUsers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="Districts",y="RegisteredUsers",title="TOP 10 REGISTERED USER",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
    
    
    query2 = f'''SELECT Districts, SUM(RegisteredUsers) AS RegisteredUsers
                    FROM {table_name}
                    WHERE States= '{state}'
                    GROUP BY Districts
                    ORDER BY RegisteredUsers
                    LIMIT 10;'''
                
    mycursor.execute(query2)
    Table_2 = mycursor.fetchall()
    connection.commit()

    df_2 = pd.DataFrame(Table_2, columns=("Districts","RegisteredUsers"))

    with col2:
        fig_amount_2=px.bar(df_2,x="Districts",y="RegisteredUsers",title="LAST 10 REGISTERED USER",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
        
    
    query3 = f'''SELECT Districts, AVG(RegisteredUsers) AS RegisteredUsers
                    FROM {table_name}
                    WHERE States= '{state}'
                    GROUP BY Districts
                    ORDER BY RegisteredUsers;'''
            
    mycursor.execute(query3)
    Table_3 = mycursor.fetchall()
    connection.commit()

    df_3 = pd.DataFrame(Table_3, columns=("Districts","RegisteredUsers"))


    fig_amount_3=px.bar(df_3, y="Districts", x="RegisteredUsers",title="AVERAGE OF REGISTERED USER ",hover_name="Districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)
    
    
def top_chart_appopens(table_name,state):
    connection = mysql.connector.connect(host="localhost", user="root", password="12345", database="phonepay_data")
    mycursor = connection.cursor()

    query1 = f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                    FROM {table_name}
                    WHERE States= '{state}'
                    GROUP BY Districts
                    ORDER BY AppOpens DESC
                    LIMIT 10;'''
                
    mycursor.execute(query1)
    Table_1 = mycursor.fetchall()
    connection.commit()

    df_1 = pd.DataFrame(Table_1, columns=("Districts","AppOpens"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="Districts",y="AppOpens",title="TOP 10 APPOPENS",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
    
    
    query2 = f'''SELECT Districts, SUM(AppOpens) AS AppOpens
                    FROM {table_name}
                    WHERE States= '{state}'
                    GROUP BY Districts
                    ORDER BY AppOpens
                    LIMIT 10;'''
                
    mycursor.execute(query2)
    Table_2 = mycursor.fetchall()
    connection.commit()

    df_2 = pd.DataFrame(Table_2, columns=("Districts","AppOpens"))

    with col2:
        fig_amount_2=px.bar(df_2,x="Districts",y="AppOpens",title="LAST 10 APPOPENS",hover_name="Districts",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
    
    
    query3 = f'''SELECT Districts, AVG(AppOpens) AS AppOpens
                    FROM {table_name}
                    WHERE States= '{state}'
                    GROUP BY Districts
                    ORDER BY AppOpens;'''
            
    mycursor.execute(query3)
    Table_3 = mycursor.fetchall()
    connection.commit()

    df_3 = pd.DataFrame(Table_3, columns=("Districts","AppOpens"))


    fig_amount_3=px.bar(df_3, y="Districts", x="AppOpens",title="AVERAGE OF APPOPENS ",hover_name="Districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)
    
    
def top_chart_registered_users(table_name):
    connection = mysql.connector.connect(host="localhost", user="root", password="12345", database="phonepay_data")
    mycursor = connection.cursor()

    query1 = f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
                    FROM {table_name}
                    GROUP BY States
                    ORDER BY RegisteredUsers DESC
                    LIMIT 10;'''
                
    mycursor.execute(query1)
    Table_1 = mycursor.fetchall()
    connection.commit()

    df_1 = pd.DataFrame(Table_1, columns=("States","RegisteredUsers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="States",y="RegisteredUsers",title="TOP 10 REGISTERED USER",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
    
    
    query2 = f'''SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
                    FROM {table_name}
                    GROUP BY States
                    ORDER BY RegisteredUsers
                    LIMIT 10;'''
                
    mycursor.execute(query2)
    Table_2 = mycursor.fetchall()
    connection.commit()

    df_2 = pd.DataFrame(Table_2, columns=("States","RegisteredUsers"))

    with col2:
        fig_amount_2=px.bar(df_2,x="States",y="RegisteredUsers",title="LAST 10 REGISTERED USER",hover_name="States",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600)
        st.plotly_chart(fig_amount_2)
        
    
    query3 = f'''SELECT States, AVG(RegisteredUsers) AS RegisteredUsers
                    FROM {table_name}
                    GROUP BY States
                    ORDER BY RegisteredUsers;'''
            
    mycursor.execute(query3)
    Table_3 = mycursor.fetchall()
    connection.commit()

    df_3 = pd.DataFrame(Table_3, columns=("States","RegisteredUsers"))


    fig_amount_3=px.bar(df_3, y="States", x="RegisteredUsers",title="AVERAGE OF REGISTERED USER ",hover_name="States",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=800,width=1000)
    st.plotly_chart(fig_amount_3)
   

    
    
    

  
    
    
    
#streamlit part

st.set_page_config(layout= "wide")
st.title(":violet[PHONEPE DATA VISUALIZATION AND EXPLORATION]")
st.write("")

with st.sidebar:
    
    
    select=option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])
    
if select== "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header(":violet[PHONEPE]")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePay is a cutting-edge mobile payment platform revolutionizing the way people transact and engage with digital financial services.")
        st.write("****FEATURES****:")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
       
        
    with col2:
        st.video("C:\\Users\\nicol\\capstone project\\phonepeproject\\Phone Pe Ad2.mp4")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        
    col3,col4= st.columns(2)
        
    with col3:
        st.video("C:\\Users\\nicol\\capstone project\\phonepeproject\Phonepay ad1.mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        #st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        #st.write("****1.Direct Transfer & More****")
        #st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")
        
    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video("C:\\Users\\nicol\\capstone project\\phonepeproject\\PhonePe Motion Graphics3.mp4")

    

elif select== "DATA EXPLORATION":
    
    tab1,tab2,tab3 = st.tabs(["AGGREGATED ANALYSIS", "MAP ANALYSIS", "TOP ANALYSIS"])
    
    with tab1:
        method=st.radio("Select The Method",["Insurance Analysis","Transaction Analysis", "User Analysis"])
        
        if method == "Insurance Analysis":
            
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year", Aggregated_insurance["Years"].min(), Aggregated_insurance["Years"].max(), Aggregated_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggregated_insurance,years)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(), tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)    
            
        elif method == "Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(), Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States", Aggre_tran_tac_Y["States"].unique())
            Aggre_tran_transaction_type(Aggre_tran_tac_Y, states)    
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter", Aggre_tran_tac_Y["Quarter"].min(), Aggre_tran_tac_Y["Quarter"].max(), Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_ty", Aggre_tran_tac_Y_Q["States"].unique())
            Aggre_tran_transaction_type(Aggre_tran_tac_Y_Q, states)
            
        elif method == "User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year", aggregated_user["Years"].min(), aggregated_user["Years"].max(), aggregated_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(aggregated_user, years)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter", Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_ty", Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
        
        
    with tab2:
        method2=st.radio("Select The Method",["Map Insurance","Map Transaction", "Map user"])
        
        if method2 == "Map Insurance":
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year_mi", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min())
            Map_insur_tac_Y=Transaction_amount_count_Y(map_insurance,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_mi", Map_insur_tac_Y["States"].unique())
            Map_insur_District(Map_insur_tac_Y, states)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter_mi", Map_insur_tac_Y["Quarter"].min(), Map_insur_tac_Y["Quarter"].max(), Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(Map_insur_tac_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_ty", Map_insur_tac_Y_Q["States"].unique())
            Map_insur_District(Map_insur_tac_Y_Q, states)
                
            
            
        elif method2 == "Map Transaction":
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year_mt", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min())
            Map_tran_tac_Y=Transaction_amount_count_Y(map_transaction,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_mt", Map_tran_tac_Y["States"].unique())
            Map_insur_District(Map_tran_tac_Y, states)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter_mt", Map_tran_tac_Y["Quarter"].min(), Map_tran_tac_Y["Quarter"].max(), Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_mi", Map_tran_tac_Y_Q["States"].unique())
            Map_insur_District(Map_tran_tac_Y_Q, states)
                
            
        elif method2 == "Map user":
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year_mu", map_user["Years"].min(), map_user["Years"].max(), map_user["Years"].min())
            map_user_Y=map_user_plot_1(map_user, years)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter_mu", map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(), map_user_Y["Quarter"].min())
            map_user_Y_Q=map_user_plot_2(map_user_Y, quarters)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_mu", map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, states)
            
            
                          
           
                        
        
    with tab3:
        method3=st.radio("Select The Method",["Top Insurance","Top Transaction", "Top user"])
        
        if method3 == "Top Insurance":
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year_ti", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min())
            top_insur_tac_Y=Transaction_amount_count_Y(top_insurance,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_ti", top_insur_tac_Y["States"].unique())
            top_insurance_plot_1(top_insur_tac_Y, states)
            
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter_ti", top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(), top_insur_tac_Y["Quarter"].min())
            top_insur_tac_Y_Q=Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)
            
            
        elif method3 == "Top Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year_tt", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min())
            top_tran_tac_Y=Transaction_amount_count_Y(top_transaction,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_tt", top_tran_tac_Y["States"].unique())
            top_insurance_plot_1(top_tran_tac_Y, states)
            
            
            col1,col2 = st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter_tt", top_tran_tac_Y["Quarter"].min(), top_tran_tac_Y["Quarter"].max(), top_tran_tac_Y["Quarter"].min())
            top_tran_tac_Y_Q=Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)
            
        elif method3 == "Top user":
            
            col1,col2 = st.columns(2)
            with col1:
                years= st.slider("Select the Year_tu", top_user["Years"].min(), top_user["Years"].max(), top_user["Years"].min())
            top_user_Y=top_user_plot_1(top_user,years)
            
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the States_tt", top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, states)
            
            
            
        
elif select== "TOP CHARTS":
    
    
    question = st.selectbox("Select the Question",["1. Transaction Amount and Transaction Count of Aggregated Insurance",
                                                   "2. Transaction Amount and Transaction Count of Map Insurance",
                                                   "3. Transaction Amount and Transaction Count of Top Insurance",
                                                   "4. Transaction Amount and Transaction Count of Aggregated Transaction",
                                                   "5. Transaction Amount and Transaction Count of Map Transaction",
                                                   "6. Transaction Amount and Transaction Count of Top Transaction",
                                                   "7. Transaction Count of Aggregated User",
                                                   "8. Registered Users of Map User",
                                                   "9. Appopens of Map Users",
                                                   "10. Registered Users of Top Users"])
    
    if question == "1. Transaction Amount and Transaction Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")
        
        

    elif question == "2. Transaction Amount and Transaction Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
        
    elif question == "3. Transaction Amount and Transaction Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")
        

    elif question == "4. Transaction Amount and Transaction Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction") 
        
    elif question == "5. Transaction Amount and Transaction Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")
        
    elif question == "6. Transaction Amount and Transaction Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")
        
    elif question == "7. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
        
    elif question == "8. Registered Users of Map User":
        
        states =st.selectbox("Select the State", map_user["States"].unique())
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user",states)
        

    elif question == "9. Appopens of Map Users":
        
        states =st.selectbox("Select the State", map_user["States"].unique())
        
        st.subheader("APPOPENS")
        top_chart_appopens("map_user",states)
        
    elif question == "10. Registered Users of Top Users":
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")
        


