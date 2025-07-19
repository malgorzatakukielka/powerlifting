import streamlit as st

st.set_page_config(page_title="Powerlifting App", page_icon=":material/exercise:", layout="wide")

st.title("Welcome to the Powerlifting Data Analysis App")
st.markdown("Use the sidebar to navigate to different analyses.")

st.write("DEBUG: session_state snapshot:", dict(st.session_state))
sex = st.session_state.get("sex")
weight_class_type = st.session_state.get("weight_class_type")
weight_class = st.session_state.get("weight_class")

st.write("Current filters:")
st.write("Sex:", st.session_state.get('sex'))
st.write("Weight class type:", st.session_state.get('weight_class_type'))
st.write("Weight class:", st.session_state.get('weight_class'))