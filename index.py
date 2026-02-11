import streamlit as st
import pyfiglet
import time

# set page config (optional)
st.set_page_config(page_title="Good Night", page_icon="🌙")

def good_night_streamlit():
    # Center the title
    st.markdown("<h1 style='text-align: center; color: cyan;'>🌙 Good Night 🌙</h1>", unsafe_allow_html=True)
    
    # Generate ASCII Art
    ascii_art = pyfiglet.figlet_format("Good Night", font="starwars")
    ascii_name = pyfiglet.figlet_format("Brother Saim", font="slant")

    # Display the ASCII art using st.text (preserves spacing)
    # We use a code block or preformatted text to ensure it aligns correctly
    st.text(ascii_art)
    
    # Add a small delay for effect (optional)
    time.sleep(0.5)
    
    st.text(ascii_name)
    
    # Add a nice message
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: yellow;'>Rest well and dream big. See you tomorrow! ✨</h3>", unsafe_allow_html=True)
    
    # Button to trigger balloons
    if st.button("Say Goodnight"):
        st.balloons()
        st.success("Sleep tight, Brother Saim!")

if __name__ == "__main__":
    good_night_streamlit()
