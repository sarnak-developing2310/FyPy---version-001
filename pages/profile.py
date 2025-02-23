import streamlit as st

def render():
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.header("User Profile")
    st.markdown("""
    <div style="display: flex; align-items: center; margin-top: 20px;">
        <img src="https://via.placeholder.com/100" class="icon-3d" style="border-radius: 50%; margin-right: 20px;">
        <div>
            <h2 style="margin: 0;">Jane Doe</h2>
            <p style="margin: 0; color: #555;">jane.doe@example.com</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("Manage your profile details, update your password, and review your account activity here.")
    st.markdown("</div>", unsafe_allow_html=True)
    