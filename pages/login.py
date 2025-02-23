import streamlit as st

def render():
    st.markdown("<div class='fade-in card' style='padding:20px;'>", unsafe_allow_html=True)
    st.header("Login")
    st.write("Enter your username and password to log in.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # In this simplified workflow we assume that the signup page
        # has stored the user data in st.session_state["user"]
        if "user" not in st.session_state:
            st.error("No registered user found. Please sign up first.")
        else:
            user = st.session_state["user"]
            # Direct plain text verification without any hashing
            if username == user.get("username") and password == user.get("password"):
                st.success("Login successful!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("Incorrect username or password.")

    st.markdown("</div>", unsafe_allow_html=True)