import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

conn = sqlite3.connect("toyota_dss.db", check_same_thread=False)
cursor = conn.cursor()

st.title("Toyota Decision Support System")

menu = st.sidebar.selectbox(
"Navigation",
["Login","Quick Access","EV Smart Routing","Sales Forecasting","Parts Procurement"]
)

# ---------------- LOGIN ---------------- #

if menu == "Login":

    st.subheader("EV Owner Login")

    email = st.text_input("Email")
    password = st.text_input("Password",type="password")

    if st.button("Login"):

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password))

        user = cursor.fetchone()

        if user:
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")


# ---------------- QUICK ACCESS ---------------- #

elif menu == "Quick Access":

    st.subheader("System Overview")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.info("EV Smart Routing")
        st.write("Locate nearest charging stations based on battery health")

    with col2:
        st.success("Sales Forecasting")
        st.write("Visualize Toyota global sales trends")

    with col3:
        st.warning("Parts Procurement")
        st.write("Analyze EV supply vs demand")


# ---------------- EV SMART ROUTING ---------------- #

elif menu == "EV Smart Routing":

    st.subheader("EV Charging Stations Map")

    battery = st.slider("Battery Health %",0,100,50)

    cursor.execute("SELECT * FROM ev_stations")
    data = cursor.fetchall()

    map = folium.Map(location=[14.5995,120.9842], zoom_start=12)

    for station in data:
        folium.Marker(
            [station[2],station[3]],
            popup=station[1],
            icon=folium.Icon(color="green")
        ).add_to(map)

    st_folium(map,width=700)


# ---------------- SALES FORECASTING ---------------- #

elif menu == "Sales Forecasting":

    st.subheader("Toyota Sales Forecast")

    df = pd.read_sql_query("SELECT * FROM sales",conn)

    fig = px.line(df,x="year",y="sales",
    title="Toyota Global Sales")

    st.plotly_chart(fig)


# ---------------- PARTS PROCUREMENT ---------------- #

elif menu == "Parts Procurement":

    st.subheader("EV Parts Supply vs Demand")

    df = pd.read_sql_query("SELECT * FROM parts_procurement",conn)

    fig = px.bar(
        df,
        x="part_name",
        y=["supply","demand"],
        barmode="group",
        title="EV Parts Supply vs Demand"
    )

    st.plotly_chart(fig)
