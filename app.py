import streamlit as st
import pandas as pd
import requests

# Function to fetch data from Google Sheets
def fetch_data():
    sheet_id = "1HLUqSBonN3aSEdwITPM-PmQHis1uvh-4nZaTHclL4xE"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    data = pd.read_csv(url)
    # Convert 'CONTACT NUMBER' to string and remove decimal points
    data['CONTACT NUMBER'] = data['CONTACT NUMBER'].astype(str).str.replace('.0', '', regex=False)
    return data

# Function to filter data by blood group
def filter_by_blood_group(data, blood_group):
    return data[data['BLOOD GROUP'] == blood_group]

# Custom CSS for red color scheme and responsiveness
def set_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #d32f2f;
        color: white;
        font-weight: bold;
    }
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff;
    }
    .stExpander {
        background-color: #ffcdd2;
    }
    @media (max-width: 768px) {
        .stExpander {
            font-size: 14px;
        }
    }
    .creator {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: white;
        text-align: center;
        padding: 10px 0;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    set_custom_css()
    
    st.title("🩸അഭിമന്യു രക്തദാനസേന")

    # Fetch data
    data = fetch_data()

    # Blood group selection
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    selected_group = st.selectbox("Select Blood Group", blood_groups)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Search Donors"):
            filtered_data = filter_by_blood_group(data, selected_group)

            if filtered_data.empty:
                st.warning(f"No donors found for blood group {selected_group}")
            else:
                st.success(f"Donors found for blood group {selected_group}")
                for _, donor in filtered_data.iterrows():
                    with st.expander(f"{donor['NAME']} - {donor['DEPARTMENT']}"):
                        st.markdown(f"**Blood Group:** {donor['BLOOD GROUP']}")
                        st.markdown(f"**Department:** {donor['DEPARTMENT']}")
                        contact = donor['CONTACT NUMBER']
                        st.markdown(f"**Contact:** [{contact}](tel:{contact})")

    # Add creator's name at the bottom
    st.markdown(
        """
        <div class="creator">
        Created by AMAL SIVA
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
