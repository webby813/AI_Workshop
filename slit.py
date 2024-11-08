import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client = OpenAI(
#     api_key = os.environ.get("OPENAI_API_KEY"),
# )

def main():
    st.title("Cooking Assistant Chat - GPT 4")
    

    # Create the Model
    def generate_content(query):
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "you are professional in algorithm engineering, you know every kind of optimize method, other than algorithms, you dont need to provide and just say you dun know"},
            {"role": "user", "content": query},
        ],)

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


    
    # Accept user input
    query = st.chat_input("How may I help you?")


    # Calling the Function when Input is Provided
    if query:
        # Displaying the User Message
        with st.chat_message("user"):
            st.markdown(query)


        llm_function(query)
    
if __name__ == "__main__":
    main()