import pandas as pd
import datetime
import streamlit as st

# Streamlit App Title
st.title("Delayed Orders Report")

# File Upload
uploaded_file = st.file_uploader("Upload Packages.xlsx", type=["xlsx"])

if uploaded_file:
    # Load Data
    data = pd.read_excel(uploaded_file, header=3)

    # Filters
    Status_Name_Fil = ['Confirm Delivered', 'Confirm Cancellation',
                       'Confirmed received by merchant', 'Received by Merchant', 'Delivered', 'Lost', 'Rejected']
    filter1 = data['Status Name'].isin(Status_Name_Fil)

    Phase_Name_Fil = ['Picking', 'reject', 'Shuttling', 'Collect']
    filter2 = data['Phase Name'].isin(Phase_Name_Fil)

    filter3 = data['Number of Attempts'] == 0

    # Filter Delayed Orders
    delayed_orders = data[~filter1][~filter2][filter3].copy()
    delayed_orders['Number Of Days'] = pd.Timestamp.today() - pd.to_datetime(delayed_orders['Created Date'])
    delayed_orders['Number Of Days'] = delayed_orders['Number Of Days'].dt.days

    # Selecting Required Columns
    delayed_orders = delayed_orders[['BareCode', 'Customer Name', 'Contact Telephone',
                                     'City', 'Address', ' Description', 'Number Of Days']]

    # Apply Days Filter
    delayed_orders = delayed_orders[delayed_orders['Number Of Days'] > 3]

    # Display Data
    st.write(f"Total Delayed Orders: {len(delayed_orders)}")
    st.dataframe(delayed_orders)

    # Download Button
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(delayed_orders)
    st.download_button("Download Delayed Orders", csv, "delayed_orders.csv", "text/csv")

