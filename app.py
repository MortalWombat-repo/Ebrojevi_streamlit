import streamlit as st
import requests
import pandas as pd

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
        with st.form(key="scan_tab"):
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


    # Define the API URL
    api_from_db = "https://ebrojevi-fast-api.onrender.com/database"


    # Create a form
    with list_tab:
        response = requests.get(api_from_db)

        # Function to color rows based on some condition (example: coloring rows with a specific column value)
        def color_rows(row):
            if row['color'] == 'Green':
                return ['background-color: #C1E1C1'] * len(row)
            if row['color'] == 'Yellow':
                return ['background-color: #FFFAA0'] * len(row)
            if row['color'] == 'Red':
                return ['background-color: #FAA0A0'] * len(row)
            else:
                return [''] * len(row)

        if response.status_code == 200:
                # Parse the JSON response
                data = response.json()

                # Convert the data to a pandas DataFrame (assuming it's a list of dictionaries)
                df = pd.DataFrame(data)

                df.reset_index(drop=True, inplace=True)
                df.index += 1  # Make the index start from 1

                # Show the DataFrame as a table, starting with the first 20 rows
                st.subheader("Additives List")
                st.write("Displaying the first 10 rows of the table. The entire database is scrollable.")
                st.write("Use the search icon in the upper right corner of the table to search by a specific name.")

                # Apply the coloring function
                styled_df = df.style.apply(color_rows, axis=1)

                # Add an option to show the full DataFrame (optional)
                #if len(df) > 5:
                    #show_full_df = st.checkbox("Show full data")
                    #if show_full_df:
                        #st.dataframe(df)  # Display the entire DataFrame when the checkbox is selected

                st.dataframe(styled_df)  # Displaying the styled dataframe

                # Show a color legend with a description
                st.subheader("Legend")
                st.write("""
                    This is a color legend to explain the meaning of each color:
                """)

                # Display color blocks and their meaning
                st.markdown("""
                    - <span style="background-color:#C1E1C1; padding: 5px 15px; border-radius: 5px;">Additives to be considered safe</span>
                """, unsafe_allow_html=True)

                # You can add more colors as needed for your other conditions:
                st.markdown("""
                    - <span style="background-color:#FFFAA0; padding: 5px 15px; border-radius: 5px;">Should not be consumed often</span>
                """, unsafe_allow_html=True)

                # Add additional colors to the legend if necessary
                st.markdown("""
                    - <span style="background-color:#FAA0A0; padding: 5px 15px; border-radius: 5px;">Should be avoided</span>
                """, unsafe_allow_html=True)
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
