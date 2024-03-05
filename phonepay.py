import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import requests
import json
 

connection = mysql.connector.connect(host="localhost", user="root", password="12345", database="phonepay_data")
mycursor = connection.cursor()

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

#top_transaction df

mycursor.execute("select * from top_transaction")
#connection.commit()
table5=mycursor.fetchall()

Top_transaction=pd.DataFrame(table5,columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_user df

mycursor.execute("select * from top_user")
#connection.commit()
table6=mycursor.fetchall()

Top_user=pd.DataFrame(table6,columns=("States", "Years", "Quarter", "Pincodes",
                                               "RegisteredUsers"))




def Transaction_amount_count_Y(df,year):
    
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg, x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)
        

    with col2:
        fig_count=px.bar(tacyg, x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)
        
    
    col1,col2=st.columns(2)
    with col1: 
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States",title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(tacyg,geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States",title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
        
    return tacy


def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2= st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)
    
    col1,col2= st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_2=px.choropleth(tacyg,geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
        
    return tacy

       

def Aggre_Tran_Transaction_type(df, state):

    tacy=df[df["States"]== state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame=tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width=600, title= f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)
        
    with col2:
        fig_pie_2= px.pie(data_frame=tacyg, names= "Transaction_type", values= "Transaction_count",
                        width=600, title= f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)


#Aggre_user_analysis_1

def Aggre_user_plot_1(df, year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)


    fig_bar_1= px.bar(aguyg, x="Brands", y="Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)


    fig_bar_1= px.bar(aguyqg, x="Brands", y="Transaction_count", title= f"{quarter} Quarter, BRANDS AND TRANSACTION COUNT",
                        width=1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguyq  


#Aggre_user_analysis_3
def Aggre_user_plot_3(df, state):
    auyqs=df[df["States"]== state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1= px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage",
                        title=f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE", width=1000,markers=True)
    st.plotly_chart(fig_line_1)
    
    
#map_transaction_district
def Map_tran_Districts(df, state):

    tacy=df[df["States"]== state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount",y= "Districts", orientation= "h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Mint_r,height=600)
        st.plotly_chart(fig_bar_1)  

    with col2:
        fig_bar_2= px.bar(tacyg, x= "Transaction_count",y= "Districts", orientation= "h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r,height=600)
        st.plotly_chart(fig_bar_2)  
    
    
      

# map_user_plot_1
def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)

    muyg= muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)


    fig_line_1= px.line(muyg, x="States", y=["RegisteredUsers","AppOpens"],
                            title=f"{year} REGISTER USER AND APPOPENS", width=800,height=800,markers=True)
    st.plotly_chart(fig_line_1)
    
    return muy  

  
# map_user_plot_2
def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg= muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)


    fig_line_1= px.line(muyqg, x="States", y=["RegisteredUsers","AppOpens"],
                            title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTER USER AND APPOPENS", width=800,height=800,markers=True,
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)
    
    return muyq 


#map_user_plot_3
def map_user_plot_3(df, states):
    muyqs=df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation="h",
                                title=f"{states.upper()} REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)
        
        
    with col2:
        fig_map_user_bar_2=px.bar(muyqs, x="AppOpens", y="Districts", orientation="h",
                                title=f"{states.upper()} APPOPENS", height=800, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)
       
#Top_tran_plot_1
def top_tran_plot_1(df, state):
    tty=df[df["States"]==state]
    tty.reset_index(drop=True, inplace=True)

    ttyg= tty.groupby("Pincodes")[["Transaction_count","Transaction_amount"]].sum()
    ttyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_top_tran_bar_1=px.bar(tty, x="Quarter", y="Transaction_amount", hover_data="Pincodes",
                                    title="TRANSACTION AMOUNT", height=650,width=600, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_tran_bar_1)
    
    with col2:
        fig_top_tran_bar_2=px.bar(tty, x="Quarter", y="Transaction_count", hover_data="Pincodes",
                                    title="TRANSACTION COUNT", height=650,width=600, color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_tran_bar_2)
    
    
def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)


    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)


    fig_top_plot_1=px.bar(tuyg, x="States",y="RegisteredUsers", color="Quarter",width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)
    return tuy


#top_user_plot_2
def top_user_plot_2(df, state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True, inplace=True)


    fig_top_plot_2=px.bar(tuys, x="Quarter", y="RegisteredUsers", title= "REGISTERED USERS, PINCODES, QUARTER",
                        width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)


def ques1():
    brand= aggregated_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index().head(10)

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                        title= "Top 10 Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)


def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)


def ques3():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def ques5():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index().head(10)

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index().head(10)

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)


def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)


def ques10():
    dt= map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)
    
    
#streamlit_part

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
        method=st.radio("Select The Method",["Transaction Analysis", "User Analysis"])
        
        if method=="Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction,years)
            
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States",Aggre_tran_tac_Y["States"].unique())
                
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)
            
            
            col1,col2=st.columns(2)
            with col1:    
               quarters= st.slider("Select the Quarters",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States_Ty ",Aggre_tran_tac_Y_Q["States"].unique())
                
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)
            
             
             
               
        
        elif method=="User Analysis":
            col1,col2=st.columns(2)
            with col1:
                
                years= st.slider("Select the Year",aggregated_user["Years"].min(),aggregated_user["Years"].max(),aggregated_user["Years"].min())
            Aggre_user_Y= Aggre_user_plot_1(aggregated_user, years)
        
            col1,col2=st.columns(2)
            with col1: 
                   
               quarters= st.slider("Select the Quarters",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y,quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States",Aggre_user_Y_Q["States"].unique())
                
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
            
        
        
    with tab2:
        method2=st.radio("Select The Method",["Map Transaction", "Map user"])
        
        if method2=="Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Year_mt",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min(),)
            Map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)
            
        
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States_mt",Map_tran_tac_Y["States"].unique())
                
            Map_tran_Districts(Map_tran_tac_Y, states)

            col1,col2=st.columns(2)
            with col1:    
               quarters= st.slider("Select the Quarters_mt",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Map_tran_tac_Y,quarters)
            
            
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States_mt ",Map_tran_tac_Y_Q["States"].unique())
                
            Map_tran_Districts(Map_tran_tac_Y_Q, states)
            
            
            
        elif method2=="Map user":
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Year_mu",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min(),)
            Map_user_Y= map_user_plot_1(map_user, years)
            
            col1,col2=st.columns(2)
            with col1:    
               quarters= st.slider("Select the Quarters_mu",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_User_tac_Y_Q= map_user_plot_2(Map_user_Y,quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States_mu ",Map_User_tac_Y_Q["States"].unique())
                
            map_user_plot_3(Map_User_tac_Y_Q, states)
        
    with tab3:
        
        method3=st.radio("Select The Method",["Top Transaction", "Top user"])

        if method3=="Top Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Year_tt",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min(),)
            Top_tran_tac_Y= Transaction_amount_count_Y(Top_transaction,years)
            
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States_tt",Top_tran_tac_Y["States"].unique())
                
            top_tran_plot_1(Top_tran_tac_Y, states)
            
            col1,col2=st.columns(2)
            with col1:    
               quarters= st.slider("Select the Quarters_tt",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Top_tran_tac_Y,quarters)
        
        elif method3=="Top user":
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Year_tu",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min(),)
            Top_User_Y= top_user_plot_1(Top_user,years)
            
            col1,col2=st.columns(2)
            with col1:
                states= st.selectbox("Select the States_tu",Top_User_Y["States"].unique())
            top_user_plot_2(Top_User_Y, states)
    
        

elif select== "TOP CHARTS":
    ques= st.selectbox("**Select the Question**",('Top 10 Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top 10 Brands Of Mobiles Used":
        ques1()
        
    elif ques=="States With Lowest Trasaction Amount":
        ques2()
        
    elif ques=="Districts With Highest Transaction Amount":
        ques3()
        
    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()
        
    elif ques=="Top 10 States With AppOpens":
        ques5()
        
    elif ques=="Least 10 States With AppOpens":
        ques6()
        
    elif ques=="States With Lowest Trasaction Count":
        ques7()
        
    elif ques=="States With Highest Trasaction Count":
        ques8()
        
    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()