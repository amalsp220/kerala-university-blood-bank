import streamlit as st
import pandas as pd
import datetime
from db_functions import add_donor, get_donors_by_blood_group, update_donor_status, get_donor_by_contact_and_department, check_and_update_status

# Streamlit app
st.set_page_config(page_title="Kerala University Blood Bank", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-title {
        color: #880808;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1em;
    }
    .sub-title {
        color: #880808;
        font-size: 1.5em;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 1em;
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        background-color: #880808;
        color: white;
    }
    .stRadio>div {
        display: flex;
        justify-content: space-evenly;
    }
    .stRadio>div>label {
        margin-right: 1em;
    }
    .stRadio>div>div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main title
st.markdown("<h1 class='main-title'>Kerala University Blood Bank</h1>", unsafe_allow_html=True)

# Sidebar menu
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False, donor=None))

option = st.sidebar.selectbox("Choose an option", ["Student Donor Registration", "Find a Donor", "Donor Login"])

check_and_update_status()

# Student Donor Registration
if option == "Student Donor Registration":
    st.markdown("<h2 class='sub-title'>Student Donor Registration</h2>", unsafe_allow_html=True)
    with st.form("registration_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=18, max_value=65)
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        department = st.selectbox("Department", ["Department of Mathematics", "Department of Physics", "Department of Chemistry"])
        contact_number = st.text_input("Contact Number")
        submitted = st.form_submit_button("Register")
        
        if submitted:
            add_donor(name, age, blood_group, department, contact_number)
            st.success("You have successfully registered as a donor!")

# Find a Donor
elif option == "Find a Donor":
    st.markdown("<h2 class='sub-title'>Find a Donor</h2>", unsafe_allow_html=True)
    blood_group = st.selectbox("Select Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    search = st.button("Search")
    
    if search:
        matching_donors = get_donors_by_blood_group(blood_group)
        for donor in matching_donors:
            status_color = "green" if donor[6] == "Ready to Donate" else "red"
            st.write(f"**Name:** {donor[1]}")
            st.write(f"**Age:** {donor[2]}")
            st.write(f"**Department:** {donor[4]}")
            st.write(f"**Contact Number:** {donor[5]}")
            st.markdown(f"<span style='color:{status_color};'>**Status:** {donor[6]}</span>", unsafe_allow_html=True)
            st.write("---")

# Donor Login
elif option == "Donor Login" and not st.session_state.logged_in:
    st.markdown("<h2 class='sub-title'>Donor Login</h2>", unsafe_allow_html=True)
    phone_number = st.text_input("Phone Number")
    department = st.selectbox("Department", ["Department of Mathematics", "Department of Physics", "Department of Chemistry"])
    login = st.button("Login")
    
    if login:
        donor = get_donor_by_contact_and_department(phone_number, department)
        if donor:
            st.session_state.logged_in = True
            st.session_state.donor = donor
            st.success("Logged in successfully!")
        else:
            st.error("Donor not found. Please check your contact number and department.")

if option == "Donor Login" and st.session_state.logged_in:
    donor = st.session_state.donor
    st.markdown("<h2 class='sub-title'>Update Status</h2>", unsafe_allow_html=True)
    st.write(f"**Name:** {donor[1]}")
    st.write(f"**Age:** {donor[2]}")
    st.write(f"**Blood Group:** {donor[3]}")
    st.write(f"**Department:** {donor[4]}")
    st.write(f"**Contact Number:** {donor[5]}")
    
    status = "Ready to Donate" if donor[6] == "Ready to Donate" else "Donated"
    status_color = "green" if status == "Ready to Donate" else "red"
    st.markdown(f"<span style='color:{status_color};'>**Current Status:** {status}</span>", unsafe_allow_html=True)
    
    status_button = st.radio("Update Status", ["I am ready to donate", "I have donated"], index=0 if status == "Ready to Donate" else 1)
    save_status = st.button("Save Status")
    
    if save_status:
        new_status = "Ready to Donate" if status_button == "I am ready to donate" else "Donated"
        last_donation_date = None if new_status == "Ready to Donate" else datetime.date.today().strftime('%Y-%m-%d')
        update_donor_status(donor[5], donor[4], new_status, last_donation_date)
        st.session_state.donor = get_donor_by_contact_and_department(donor[5], donor[4])
        st.success("Status updated successfully!")
