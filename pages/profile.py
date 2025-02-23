import streamlit as st

def render():
    st.markdown("<div class='fade-in card' style='padding:20px;'>", unsafe_allow_html=True)
    
    st.header("User Profile")
    
    # User Information
    st.markdown("""
    <div style="display: flex; align-items: center; margin-top: 20px;">
        <img src="https://via.placeholder.com/100" class="icon-3d" style="border-radius: 50%; margin-right: 20px;">
        <div>
            <h2 style="margin: 0;">Jane Doe</h2>
            <p style="margin: 0; color: #555;">jane.doe@example.com</p>
            <p style="margin: 0; color: #777;">+91 9876543210</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Manage your profile details, update your password, and review your account activity here.")
    
    st.markdown("---")
    
    # Cash in Hand for Investment
    st.subheader("💰 Cash in Hand for Investment")
    st.write("₹ 2,50,000 available for investment.")
    
    st.markdown("---")
    
    # Customer Support Section
    st.subheader("📞 Customer Support")
    st.write("Need help? Our support team is available 24/7.")
    if st.button("Live Chat 💬"):
        st.write("Redirecting to live chat...")
    if st.button("Help Center 📚"):
        st.write("Opening Help Center...")
    
    st.markdown("---")
    
    # Report Fraud Section
    st.subheader("⚠ Report Fraud")
    st.write("If you suspect fraudulent activity, report it immediately.")
    fraud_description = st.text_area("Describe the issue:")
    if st.button("Submit Report 🚨"):
        if fraud_description:
            st.success("Your report has been submitted. Our team will investigate.")
        else:
            st.error("Please provide a description before submitting.")
    
    st.markdown("</div>", unsafe_allow_html=True)