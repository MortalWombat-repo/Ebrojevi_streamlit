import streamlit as st
import requests

# Streamlit App Configuration - This must be first
st.set_page_config(page_title="Ebrojevi", page_icon="🔍", layout="wide")

# -----------------------------------
# Streamlit UI
# -----------------------------------

def main():
    #Title page
    # Create two columns: one small for the icon, one large for the title
    col1, col2 = st.columns([1, 18])

    with col1:
        st.image("img/icon_no_background.png", width=70)

    with col2:
        st.title("Ebrojevi")  # 👈 title next to logo

    # Sidebar for settings
    with st.sidebar:
        st.markdown("### About")
        st.markdown("This web app scans the additives in food packagings and groups them by harmfulness.")
        st.markdown("[Click here to download the app for your mobile phone instead.](https://www.google.com/)")
        st.markdown("### Made By")
        st.markdown("The Ebrojevi team with ❤️")
        col1, col2 = st.columns([1, 10])
        with col1:
            st.image("img/linkedin.svg", width=20)
        with col2:
            st.markdown("[Connect with us on LinkedIn](https://www.linkedin.com/)")

    # Tabs for Search, Analysis, Visualization, and Summarization
    scan_tab, list_tab, use_ai = st.tabs(["📷 Scan", "📋 List all additives", "🤖 Explain with AI"])

    with scan_tab:
        with st.form(key="query_form"):
            # Upload image file
            uploaded_file = st.file_uploader("📷 Upload packaging image:", type=["png", "jpg", "jpeg"])

            # Optional: Preview image if uploaded
            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Packaging", use_column_width=True)

            # Submit button
            submit_button = st.form_submit_button("🔎 Start scanning...")

        # Handle form submission
        if submit_button and uploaded_file is not None:
            with st.spinner("Scanning the input..."):
                scan = scan_item(uploaded_file)  # Assuming scan_item processes the file

                # Save into session_state
                st.session_state['scan'] = scan

        # Always display article if it exists in session state
        if 'scan' in st.session_state:
            st.subheader("📖 Scan results")
            st.markdown(st.session_state['scan'])

if __name__ == "__main__":
    main()
