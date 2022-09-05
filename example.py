# streamlit_app.py

import streamlit as st
import snowflake.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_customers(customer_id):
    if customer_id is None or customer_id == 'None':
        return []
    return run_query(f"select * from customer where C_CUSTKEY='{customer_id}'")


customer_id = st.text_input('Choose a customer', None)


rows = get_customers(customer_id)

# Print results.
for row in rows:
    st.write(row)
