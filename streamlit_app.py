import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect("toyota_dss.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- SESSION ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- LOGIN PAGE ---------------- #

def login_page():

    st.title("Toyota EV Decision Support System")
    st.subheader("EV Owner Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password))

        user = cursor.fetchone()

        if user:

            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("❌ Email and Password do not match")

# ---------------- HOME PAGE ---------------- #

def home_page():

    st.title("Toyota DSS Dashboard")

    st.write("Overview of System Features")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.subheader("EV Smart Routing")
        st.write("Locate charging stations and find best route.")

        if st.button("Open EV Routing"):
            st.session_state.page = "ev_routing"
            st.rerun()

    with col2:
        st.subheader("Sales Forecasting")
        st.write("View Toyota sales trends for the past 5 years.")

        if st.button("Open Sales Forecast"):
            st.session_state.page = "sales"
            st.rerun()

    with col3:
        st.subheader("Parts Procurement")
        st.write("Analyze supply and demand of EV parts.")

        if st.button("Open Parts Procurement"):
            st.session_state.page = "parts"
            st.rerun()

# ---------------- EV ROUTING PAGE ---------------- #

def ev_routing_page():

    st.title("EV Smart Routing")

    st.subheader("Battery Status")

    battery = st.slider("Battery Level (%)",0,100,50)

    st.write("Battery Level:",battery,"%")

    st.subheader("Nearby Charging Stations")

    cursor.execute("SELECT * FROM ev_stations")
    stations = cursor.fetchall()

    map = folium.Map(location=[14.5995,120.9842], zoom_start=12)

    for station in stations:
        folium.Marker(
            [station[2],station[3]],
            popup=station[1],
            icon=folium.Icon(color="green")
        ).add_to(map)

    st_folium(map,width=700)

    st.subheader("Best Charging Suggestion")

    if battery < 30:
        st.warning("⚠ Battery Low. Recommended to go to nearest charging station immediately.")
    elif battery < 60:
        st.info("Battery is moderate. Plan charging soon.")
    else:
        st.success("Battery level is good.")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- SALES FORECAST PAGE ---------------- #

def sales_page():

    st.title("Toyota Sales Forecasting")

    df = pd.read_sql_query("SELECT * FROM sales", conn)

    fig = px.line(
        df,
        x="year",
        y="sales",
        markers=True,
        title="Toyota Sales in the Last 5 Years"
    )

    st.plotly_chart(fig)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- PARTS PROCUREMENT PAGE ---------------- #

def parts_page():

    st.title("EV Parts Procurement")

    df = pd.read_sql_query("SELECT * FROM parts_procurement", conn)

    fig = px.bar(
        df,
        x="part_name",
        y=["supply","demand"],
        barmode="group",
        title="Supply vs Demand of EV Parts"
    )

    st.plotly_chart(fig)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---------------- PAGE CONTROLLER ---------------- #

if not st.session_state.logged_in:
    login_page()

else:

    if st.session_state.page == "home":
        home_page()

    elif st.session_state.page == "ev_routing":
        ev_routing_page()

    elif st.session_state.page == "sales":
        sales_page()

    elif st.session_state.page == "parts":
        parts_page()
