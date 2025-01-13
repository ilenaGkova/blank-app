import streamlit as st

st.title("Page C")
st.write("You've reached Page B")
st.write(st.session_state.current_username)
