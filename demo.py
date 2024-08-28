from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Float, Time
import streamlit as st
import pandas as pd
import pymysql  

engine = create_engine('mysql+pymysql://root:root@localhost/RedbusInfo')

def dataBaseConnection(query):
    engine = create_engine('mysql+pymysql://root:root@localhost/RedbusInfo')
    with engine.connect() as conn:
        df = pd.read_sql(query,conn)
    return df

selectRadioVar = st.sidebar.radio("Main Menu",["Home","Search Buses"])

if selectRadioVar == "Home":    

    st.markdown(
        """
        <style>
        .container {
            display: flex;
            align-items: center;
        }
        .container img {
            margin-right: 20px; /* Adjust this value to control spacing */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="container">
            <img src="https://play-lh.googleusercontent.com/2sknePPj33W1Iu2tZbDFario3G7kpIJFkKYm9VgGnQYKzn_WJygKFihJkZTx8H7sb0o" width="100">
            <h1>Red Bus Booking Site</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### For How to Book Tickets Watch this Video")

    st.video("https://youtu.be/eyAAUGhvZu8?si=q4Ev6pbhyxX0FO7a")

    st.markdown("#### For Ticket Bookings click this link [REDBUS](https://www.redbus.in/)")

elif selectRadioVar == "Search Buses":
    st.markdown("# Find Your Buses Here :bus: :heart: ")
    with st.form("bus_inquiry"):
        col1,col2 = st.columns(2)
        sqlQuery = "select * from bus_info"
        data = dataBaseConnection(sqlQuery) 

        busRouteInfo = data["Route Name"].unique()
        ratingInfo = data["Star Rating"].unique()
        priceInfo = data["Price"].unique() 
        busNameInfo = data["Bus Name"].unique()   
        seatAvailableInfo = data["Seats Available"].unique()  

        with col1:
            routeInfo = col1.selectbox("Select the Route", busRouteInfo)
            ratings = col1.selectbox("Select the Ratings", ratingInfo)
        with col2:
            seatAvailableInfo = col2.selectbox("Select Number of Seat Availablity",seatAvailableInfo)
            price = col2.selectbox("Bus Fare Range(Start From)", priceInfo)

        submitted = st.form_submit_button("Search Buses")

        if submitted:
            searchquery = f'select * from bus_info where `Route Name` = "{routeInfo}" and `Star Rating`>={ratings} and `Seats Available`>={seatAvailableInfo} and Price>={price}'
            print(searchquery)
            searchBusInfo = dataBaseConnection(searchquery)

            bus_data = pd.DataFrame(searchBusInfo)

            if bus_data.empty:
                st.warning("No buses are Available")    
            else: 
                st.success("Available buses Listed Below")
                st.dataframe(bus_data)
