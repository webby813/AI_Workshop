import streamlit as st
from openai import OpenAI

def main():
    st.sidebar.header("Settings")
    # Add input for the user's API key at the top
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
    
    st.title("Cooking Assistant Chat - GPT 4")

    # Define the function to generate content with the user-provided API key
    def generate_content(query):
        # Ensure the user has provided an API key
        if not api_key:
            st.error("Please enter your OpenAI API Key.")
            return "API Key not provided."

        # Create the client with the provided API key
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are professional in algorithm engineering. Provide optimized methods only for algorithms."},
                {"role": "user", "content": query},
            ],
        )
        return response.choices[0].message.content
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role":"assistant",
                "content":"Ask me Anything"
            }
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process and store Query and Response
    def llm_function(query):
        response = generate_content(query)
        # Displaying the Assistant Message
        with st.chat_message("assistant"):
            st.markdown(response)
        # Storing the User Message
        st.session_state.messages.append(
            {
                "role":"user",
                "content": query
            }
        )
        # Storing the Assistant Message
        st.session_state.messages.append(
            {
                "role":"assistant",
                "content": response
            }
        )

    query = st.chat_input("How may I help you?")

    # Calling the Function when Input is Provided
    if query:
        with st.chat_message("user"):
            st.markdown(query)
        llm_function(query)
    
if __name__ == "__main__":
    main()
