import streamlit as st

def render():
    st.markdown("<div class='fade-in card' style='padding:20px;'>", unsafe_allow_html=True)
    st.header("Sign Up")
    st.write("Create a new account:")

    name = st.text_input("Full Name")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif not name or not username or not email or not password:
            st.error("Please fill in all fields.")
        else:
            # Prepare the user data document (store plain text)
            user_data = {
                "name": name,
                "username": username,
                "email": email,
                "password": password
            }
            
            # Store the user data in session state for this session
            st.session_state["user"] = user_data
            st.success("Signup successful! Please proceed to log in.")

    st.markdown("</div>", unsafe_allow_html=True)