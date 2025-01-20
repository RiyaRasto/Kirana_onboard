import streamlit as st
import sqlite3

def create_database():
    """
    Creates a database table to store seller information.
    """
    conn = sqlite3.connect('kirana_onboard.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact_number TEXT,
            email TEXT,
            store_name TEXT,
            store_address TEXT,
            gst_number TEXT,
            alt_phone TEXT,
            gender TEXT,
            dob TEXT,
            product_category TEXT,
            open_date TEXT,
            open_time TEXT,
            payment_methods TEXT 
        )
    """)

    conn.commit()
    conn.close()

def insert_seller(seller):
    """
    Inserts a new seller into the database.

    Args:
        seller (dict): A dictionary containing the seller's information.
    """
    conn = sqlite3.connect('kirana_onboard.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sellers (name, contact_number, email, store_name, store_address, gst_number, alt_phone, gender, dob, product_category, open_date, open_time, payment_methods)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        seller['name'],
        seller['contact_number'],
        seller['email'],
        seller['store_name'],
        seller['store_address'],
        seller['gst_number'],
        seller['alt_phone'],
        seller['gender'],
        str(seller['dob']),  # Convert date to string
        seller['product_category'],
        str(seller['open_date']),  # Convert date to string
        seller['open_time'],
        ','.join(seller['payment_methods'])  # Convert list to comma-separated string
    ))

    conn.commit()
    conn.close()

def get_all_sellers():
    """
    Retrieves all sellers from the database.

    Returns:
        list: A list of dictionaries, where each dictionary represents a seller.
    """
    conn = sqlite3.connect('kirana_onboard.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sellers")
    sellers = cursor.fetchall()

    conn.close()

    return sellers

def onboarding_form():
    st.title("Kirana Store Onboarding")

    create_database()  # Ensure the database and table exist

    # Session State Initialization
    st.session_state.setdefault('seller_name', "")
    st.session_state.setdefault('contact_number', "")
    st.session_state.setdefault('email', "")
    st.session_state.setdefault('store_name', "")
    st.session_state.setdefault('store_address', "")
    st.session_state.setdefault('gst_number', "")
    st.session_state.setdefault('alt_phone', "")
    st.session_state.setdefault('gender', "")
    st.session_state.setdefault('dob', None)  # Initialize as None for date input
    st.session_state.setdefault('product_category', "")
    st.session_state.setdefault('open_date', None)  # Initialize as None for date input
    st.session_state.setdefault('open_time', "")
    st.session_state.setdefault('payment_methods', [])  # Initialize as an empty list

    tabl, tab2, tab3 = st.tabs(["Personal Info", "Store Details", "Summary"])

    with tabl:
        st.subheader("Personal Information")
        seller_name = st.text_input("Seller Name")
        contact_number = st.text_input("Contact Number")
        st.markdown("### Your data is secure with us!")
        email = st.text_input("Email Address")
        gender = st.selectbox("Gender", ("Male", "Female", "Other"))
        dob = st.date_input("Date of Birth (DD/MM/YYYY)")

    with tab2:
        st.subheader("Store Details")
        store_name = st.text_input("Store Name")
        address = st.text_area("Store Address")
        product_category = st.selectbox("Primary Product Category", ["Groceries", "Vegetables", "Snacks", "Dairy", "Other"])
        open_date = st.date_input("Store Opening Date")
        open_time = st.time_input("Store Opening Time")
        payment_methods = st.multiselect("Accepted Payment Methods", ["Cash", "UPI", "Credit/Debit Card"])

    with tab3:
        st.subheader("Summary")

        if seller_name and contact_number and store_name and address:
            st.write(f"*Seller Name*: {seller_name}")
            st.write(f"*Contact Number*: {contact_number}")
            st.write(f"*Email*: {email}")
            st.write(f"*Store Name*: {store_name}")
            st.write(f"*Store Address*: {address}")
            st.write(f"*Product Category*: {product_category}")
            st.write(f"*Opening Date & Time*: {open_date} - {open_time}")
            st.write(f"*Accepted Payment Methods*: {', '.join(payment_methods)}")

        else:
            st.warning("Complete all fields to see a summary.")

        progress = 0

        if seller_name:
            progress += 20
        if contact_number:
            progress += 20
        if store_name:
            progress += 20
        if address:
            progress += 20
        if product_category and payment_methods:
            progress += 20

        st.progress(progress)

        if st.button("Submit"):
            if progress == 100:
                # Store data in session state
                st.session_state['seller_name'] = seller_name
                st.session_state['contact_number'] = contact_number
                st.session_state['email'] = email
                st.session_state['store_name'] = store_name
                st.session_state['store_address'] = address
                st.session_state['gst_number'] = gst_number
                st.session_state['alt_phone'] = alt_phone
                st.session_state['gender'] = gender
                st.session_state['dob'] = dob
                st.session_state['product_category'] = product_category
                st.session_state['open_date'] = open_date
                st.session_state['open_time'] = open_time
                st.session_state['payment_methods'] = payment_methods

                # Insert data into database
                seller_data = {
                    'name': st.session_state['seller_name'],
                    'contact_number': st.session_state['contact_number'],
                    'email': st.session_state['email'],
                    'store_name': st.session_state['store_name'],
                    'store_address': st.session_state['store_address'],
                    'gst_number': st.session_state['gst_number'],
                    'alt_phone': st.session_state['alt_phone'],
                    'gender': st.session_state['gender'],
                    'dob': str(st.session_state['dob']),
                    'product_category': st.session_state['product_category'],
                    'open_date': str(st.session_state['open_date']),
                    'open_time': st.session_state['open_time'],
                    'payment_methods': ','.join(st.session_state['payment_methods'])
                }
                insert_seller(seller_data)

                st.success("Form submitted successfully!")
                st.balloons()

            else:
                st.error("Please fill out all fields before submitting.")

if __name__ == "_main_":
    onboarding_form()