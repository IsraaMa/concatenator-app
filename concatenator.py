import streamlit as st
import pandas as pd
from io import BytesIO
import base64

def concatenate_tables(tables):
    if tables:
        concatenated_table = pd.concat(tables, ignore_index=True)
        return concatenated_table
    return None

def download_table(table, filename="concatenated_table.csv"):
    csv_file = table.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Concatenated Table</a>'
    return href


def download_table_clean(table, filename="concatenated_table.csv"):
    csv_file = table.dropna(axis=1).to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Clean Table</a>'
    return href

# Main Streamlit app
def main():
    st.title("Table Concatenator App")

    # Initialize an empty list to store uploaded tables
    uploaded_tables = []

    # Allow users to upload files
    uploaded_files = st.file_uploader("Upload Excel or CSV files", type=["xlsx", "csv"], accept_multiple_files=True)

    # Display the names of the uploaded files
    if uploaded_files:
        st.subheader("Uploaded Files:")
        for file in uploaded_files:
            st.write(file.name)

        # Concatenate tables on button click
        if st.button("Concatenate"):

            tables = []
            for file in uploaded_files:
                if file.name.endswith('.xlsx'):
                    table = pd.read_excel(file)
                else:
                    table = pd.read_csv(file)
                tables.append(table)

            uploaded_tables.extend(tables)

            # Display the concatenated table
            concatenated_table = concatenate_tables(uploaded_tables)
            st.subheader("Concatenated Table:")
            st.write(concatenated_table)

            # Enable download button if tables are concatenated
            if concatenated_table is not None:
                st.markdown(download_table(concatenated_table), unsafe_allow_html=True)
                st.markdown(download_table_clean(concatenated_table), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
