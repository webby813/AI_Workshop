import streamlit as st 

# Set the app title 
st.title('My First Streamlit App') # Display a welcome message 
st.write('Welcome to my Streamlit app!')
# Add a button 
st.button("Reset", type="primary") 
if st.button("Say hello"): 
    st.write("Why hello there") 
else: 
    st.write("Goodbye")