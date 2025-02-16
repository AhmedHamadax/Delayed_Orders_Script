import pandas as pd
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
    filter4 = data['Number of Attempts'] == 1

    def process_data(df, filter_attempts):
        filtered_df = df[~filter1][~filter2][filter_attempts].copy()

        # Correct datetime parsing
        filtered_df['Created Date'] = pd.to_datetime(
            filtered_df['Created Date'], format="%d/%m/%Y %H:%M:%S", errors='coerce'
        )

        # Calculate Number Of Days
        filtered_df['Number Of Days'] = (pd.Timestamp.today() - filtered_df['Created Date']).dt.days

        # Select relevant columns
        filtered_df = filtered_df[['BareCode', 'Customer Name', 'Contact Telephone',
                                   'City', 'Address', ' Description', 'Number Of Days']]

        return filtered_df[filtered_df['Number Of Days'] > 3]

    # Process data for both filters
    delayed_orders_0 = process_data(data, filter3)
    delayed_orders_1 = process_data(data, filter4)

    # Display Data
    st.subheader("Delayed Orders (Attempts = 0)")
    st.write(f"Total Delayed Orders: {len(delayed_orders_0)}")
    st.dataframe(delayed_orders_0)

    st.subheader("Delayed Orders (Attempts = 1)")
    st.write(f"Total Delayed Orders: {len(delayed_orders_1)}")
    st.dataframe(delayed_orders_1)

    # Download Button
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_0 = convert_df(delayed_orders_0)
    csv_1 = convert_df(delayed_orders_1)

    st.download_button("Download Delayed Orders (Attempts = 0)", csv_0, "delayed_orders_0.csv", "text/csv")
    st.download_button("Download Delayed Orders (Attempts = 1)", csv_1, "delayed_orders_1.csv", "text/csv")
