import streamlit as st
import time

# Page configuration
st.set_page_config(page_title="Good Night", page_icon="🌙")

# Styling the message with Markdown
st.markdown("<br><br>", unsafe_allow_html=True) # Add some space
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🌙 Good Night</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #FFD700;'>Brother Saim</h2>", unsafe_allow_html=True)

st.divider()

st.markdown("<p style='text-align: center; font-size: 20px;'>Rest well and dream big. See you tomorrow! ✨</p>", unsafe_allow_html=True)

# Interactive element
if st.button("Click for a sleepy surprise"):
    st.balloons()
    st.toast('Sweet dreams, Saim!', icon='😴')
    time.sleep(1)
