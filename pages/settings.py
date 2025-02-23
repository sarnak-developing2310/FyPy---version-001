import streamlit as st

def render():
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.header("Settings & Support")
    st.subheader("Account Settings")
    uname = st.text_input("Username", value="FinanceHub_User")
    mail = st.text_input("Email", value="user@example.com")
    if st.button("Update Settings"):
        st.success("Settings updated successfully! (Simulated)")
    st.subheader("Support")
    st.write("For help, contact support@financehub.com or visit our FAQ section.")
    st.markdown("</div>", unsafe_allow_html=True)