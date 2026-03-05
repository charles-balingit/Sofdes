import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# ---------------- SESSION ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- LOGIN PAGE ---------------- #

def login_page():

    st.title("Toyota Decision Support System")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Sample account for testing
    correct_email = "owner@toyota.com"
    correct_password = "12345"

    if st.button("Login"):

        if email == correct_email and password == correct_password:

            st.session_state.logged_in = True
            st.session_state.page = "home"
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("❌ Email and Password do not match")


# ---------------- HOME PAGE ---------------- #

def home_page():

    st.title("Toyota DSS Dashboard")

    st.write("Overview of the three main system features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("EV Smart Routing")
        st.write("Find nearby EV charging stations and best route.")

        if st.button("Go to EV Smart Routing"):
            st.session_state.page = "ev"
            st.rerun()

    with col2:
        st.subheader("Sales Forecasting")
        st.write("View Toyota sales for the past 5 years.")

        if st.button("Go to Sales Forecasting"):
            st.session_state.page = "sales"
            st.rerun()

    with col3:
        st.subheader("Parts Procurement")
        st.write("Analyze EV parts supply and demand.")

        if st.button("Go to Parts Procurement"):
            st.session_state.page = "parts"
            st.rerun()


# ---------------- EV ROUTING PAGE ---------------- #

def ev_page():

    st.title("EV Smart Routing")

    st.subheader("Battery Status")

    battery = st.slider("Battery Level (%)", 0, 100, 50)

    st.write("Current Battery:", battery, "%")

    st.subheader("Nearby Charging Stations")

    # Sample station data
    stations = [
        ("Pasig Charging Station", 14.5764, 121.0851),
        ("Makati EV Hub", 14.5547, 121.0244),
        ("Quezon City Station", 14.6760, 121.0437)
    ]

    m = folium.Map(location=[14.5995, 120.9842], zoom_start=12)

    for station in stations:
        folium.Marker(
            [station[1], station[2]],
            popup=station[0],
            icon=folium.Icon(color="green")
        ).add_to(m)

    st_folium(m, width=700)

    st.subheader("Charging Recommendation")

    if battery < 30:
        st.warning("Battery is low. Recommended to go to the nearest charging station.")

    elif battery < 60:
        st.info("Battery level is moderate. Plan charging soon.")

    else:
        st.success("Battery level is good.")

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ---------------- SALES PAGE ---------------- #

def sales_page():

    st.title("Toyota Sales Forecasting")

    # Sample 5 year sales data
    data = {
        "Year": [2020, 2021, 2022, 2023, 2024],
        "Sales": [9500000, 10400000, 10500000, 11200000, 11500000]
    }

    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Year",
        y="Sales",
        markers=True,
        title="Toyota Global Sales (5 Years)"
    )

    st.plotly_chart(fig)

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ---------------- PARTS PAGE ---------------- #

def parts_page():

    st.title("EV Parts Procurement")

    # Sample supply and demand
    data = {
        "Part": [
            "EV Battery Pack",
            "Electric Motor",
            "Charging Module",
            "Power Control Unit"
        ],
        "Supply": [500, 300, 200, 150],
        "Demand": [650, 280, 320, 200]
    }

    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="Part",
        y=["Supply", "Demand"],
        barmode="group",
        title="EV Parts Supply vs Demand"
    )

    st.plotly_chart(fig)

    if st.button("Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ---------------- PAGE CONTROLLER ---------------- #

if not st.session_state.logged_in:
    login_page()

else:

    if st.session_state.page == "home":
        home_page()

    elif st.session_state.page == "ev":
        ev_page()

    elif st.session_state.page == "sales":
        sales_page()

    elif st.session_state.page == "parts":
        parts_page()
