# # import smtplib

# # my_email = "test@gmail.com"
# # password = "test123"


# # connection = smtplib.SMTP("smtp.gmail.com", 587)
# # connection.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
# # connection.login(user=my_email, password=password)

# # connection.sendmail(from_addr=my_email, to_addrs="receipentemail.com", msg = "hello world")

# # connection.close()

# import streamlit as st
# import smtplib
# import ssl # For creating a secure context

# def send_email(sender_email, app_password, recipient_email, subject, body):
#     """
#     Sends an email using SMTPLIB with Gmail.
#     """
#     # Create the email message string
#     message = f"Subject: {subject}\n\n{body}"

#     try:
#         # Create a secure SSL context
#         context = ssl.create_default_context()

#         # Connect to Gmail's SMTP server
#         # 'smtp.gmail.com' is the server address, 587 is the standard TLS port
#         with smtplib.SMTP("smtp.gmail.com", 587) as connection:
#             connection.starttls(context=context) # Upgrade the connection to a secure encrypted SSL/TLS connection
#             connection.login(sender_email, app_password) # Log in using App Password
#             connection.sendmail(sender_email, recipient_email, message.encode('utf-8')) # Encode for proper handling
        
#         return True, "Email sent successfully!"
    
#     except smtplib.SMTPAuthenticationError:
#         return False, "Authentication failed. Check your Gmail address and App Password in .streamlit/secrets.toml. Remember to use an App Password if 2FA is enabled."
#     except smtplib.SMTPConnectError:
#         return False, "Could not connect to the SMTP server. Check your internet connection or server address."
#     except Exception as e:
#         return False, f"An unexpected error occurred: {e}"

# # --- Streamlit UI ---

# st.set_page_config(
#     page_title="Streamlit Email Sender",
#     layout="centered",
#     # icon="📧"
# )

# st.title("📧 Send Email with Streamlit")
# st.write("Enter the details below to send an email using your Gmail account.")

# st.markdown("---")

# # Retrieve credentials from Streamlit Secrets
# try:
#     my_email = st.secrets["gmail_email"]
#     app_password = st.secrets["gmail_app_password"]
# except KeyError:
#     st.error("Error: Gmail credentials not found in `.streamlit/secrets.toml`.")
#     st.info("Please create or update your `.streamlit/secrets.toml` file with `gmail_email` and `gmail_app_password`.")
#     st.stop() # Stop execution if credentials are not found

# st.subheader("Email Details")

# recipient_email = st.text_input("Recipient Email:", placeholder="recipient@example.com")
# subject = st.text_input("Subject:", placeholder="Hello from Streamlit!")
# body = st.text_area("Message Body:", placeholder="Type your email message here...")

# st.markdown("---")

# if st.button("🚀 Send Email", use_container_width=True):
#     if not recipient_email or not subject or not body:
#         st.warning("Please fill in all fields (Recipient, Subject, and Message Body).")
#     elif not "@" in recipient_email or not "." in recipient_email:
#         st.warning("Please enter a valid recipient email address.")
#     else:
#         with st.spinner("Sending email..."):
#             success, message = send_email(my_email, app_password, recipient_email, subject, body)
            
#             if success:
#                 st.success(message)
#                 # Clear inputs after successful send (optional)
#                 st.session_state.recipient_email = ""
#                 st.session_state.subject = ""
#                 st.session_state.body = ""
#             else:
#                 st.error(message)

# # Initialize session state for input clearing if not already set
# if "recipient_email" not in st.session_state:
#     st.session_state.recipient_email = ""
# if "subject" not in st.session_state:
#     st.session_state.subject = ""
# if "body" not in st.session_state:
#     st.session_state.body = ""

# st.markdown("""
# <style>
# .footer {
#     position: fixed;
#     left: 0;
#     bottom: 0;
#     width: 100%;
#     background-color: #f0f2f6;
#     color: #888;
#     text-align: center;
#     padding: 10px;
#     font-size: 0.8em;
# }
# </style>
# <div class="footer">
#     Created with ❤️ using Streamlit and SMTPLIB.
# </div>
# """, unsafe_allow_html=True)


import streamlit as st
import smtplib
import ssl

# Replace st.cache with st.cache_data
@st.cache_data
def send_email(sender_email, app_password, recipient_email, subject, body):
    """
    Sends an email using SMTPLIB with Gmail.
    """
    message = f"Subject: {subject}\n\n{body}"

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls(context=context)
            connection.login(sender_email, app_password)
            connection.sendmail(sender_email, recipient_email, message.encode('utf-8'))
        
        return True, "Email sent successfully!"
    
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your Gmail address and App Password in .streamlit/secrets.toml. Remember to use an App Password if 2FA is enabled."
    except smtplib.SMTPConnectError:
        return False, "Could not connect to the SMTP server. Check your internet connection or server address/port."
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

# --- Streamlit UI ---

st.set_page_config(
    page_title="Streamlit Email Sender",
    layout="centered",
    # icon="📧"
)

st.title("📧 Send Email with Streamlit")
st.write("Enter the details below to send an email using your Gmail account.")

st.markdown("---")

try:
    my_email = st.secrets["gmail_email"]
    app_password = st.secrets["gmail_app_password"]
except KeyError:
    st.error("Error: Gmail credentials not found in `.streamlit/secrets.toml`.")
    st.info("Please create or update your `.streamlit/secrets.toml` file with `gmail_email` and `gmail_app_password`.")
    st.stop()

st.subheader("Email Details")

# Use st.session_state for persistent input values
if "recipient_email" not in st.session_state:
    st.session_state.recipient_email = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "body" not in st.session_state:
    st.session_state.body = ""

recipient_email = st.text_input("Recipient Email:", value=st.session_state.recipient_email, placeholder="recipient@example.com", key="recipient_input")
subject = st.text_input("Subject:", value=st.session_state.subject, placeholder="Hello from Streamlit!", key="subject_input")
body = st.text_area("Message Body:", value=st.session_state.body, placeholder="Type your email message here...", key="body_input")

st.markdown("---")

if st.button("🚀 Send Email", use_container_width=True):
    if not recipient_email or not subject or not body:
        st.warning("Please fill in all fields (Recipient, Subject, and Message Body).")
    elif not "@" in recipient_email or not "." in recipient_email:
        st.warning("Please enter a valid recipient email address.")
    else:
        with st.spinner("Sending email..."):
            success, message = send_email(my_email, app_password, recipient_email, subject, body)
            
            if success:
                st.success(message)
                # Clear inputs after successful send
                st.session_state.recipient_email = ""
                st.session_state.subject = ""
                st.session_state.body = ""
            else:
                st.error(message)

st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f0f2f6;
    color: #888;
    text-align: center;
    padding: 10px;
    font-size: 0.8em;
}
</style>
<div class="footer">
    Created by Hadiqa Gohar ❤️.
</div>
""", unsafe_allow_html=True)
