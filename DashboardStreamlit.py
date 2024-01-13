import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:",layout="wide")

# Tytuł strony i usunięcie wolnej przestrzeni na górze
st.title(" :bar_chart: Dashboard Projekt")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)    
#st.sidebar.header("Data Picker")

# Wgranie pliku
df = pd.read_excel("Zestaw6_ETAP_2.xlsx")

col1, col2 = st.columns((2))
df["Data"] = pd.to_datetime(df["Data"])


 # WPROWADZENIE MIN I MAX DATY  
startDate = pd.to_datetime(df["Data"]).min()
endDate = pd.to_datetime(df["Data"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Data"] >= date1) & (df["Data"] <= date2)].copy()

with col1:
    st.subheader("Rzeczywisty Czas Pracy/Nominalny Czas Pracy")
    fig = px.line(df, x = "Data", y = ["Rzeczywisty Czas Pracy","Nominalny Czas Pracy"])
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Ilosc Produktow Prawidlowych/Rzeczywista Ilosc Produkcji")
    fig = px.line(df, x = "Data", y = ["Ilosc Produktow Prawidlowych","Rzeczywista Ilosc Produkcji"])
    st.plotly_chart(fig,use_container_width=True, height = 200)

# RYSOWANIE KOLEJNYCH DWOCH WYKRESOW 
cl1, cl2 = st.columns((2)) 
with cl1:
      
    df["Miesiac"] = df["Data"].dt.to_period("M")
    st.subheader('Analiza MTTR/MTTF/MTBF Miesięczna')
    linechart = pd.DataFrame(df.groupby(df["Miesiac"].dt.strftime("%Y : %b"))["MTTR","MTTF","MTBF"].sum()).reset_index()
    fig2 = px.line(linechart, x = "Miesiac", y=["MTTR","MTTF","MTBF"],height=500, width = 500,template="gridon")
    st.plotly_chart(fig2,use_container_width=True)
    
with cl2:
    df["Miesiac"] = df["Data"].dt.to_period("M")
    st.subheader('Analiza OEE Miesięczna')
    linechart = pd.DataFrame(df.groupby(df["Miesiac"].dt.strftime("%Y : %b"))["D","E","J","OEE"].sum()).reset_index()
    fig2 = px.line(linechart, x = "Miesiac", y=["D","E","J","OEE"],height=500, width = 800,template="gridon")
    st.plotly_chart(fig2,use_container_width=True)


