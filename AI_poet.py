import streamlit as st
from langchain_openai import ChatOpenAI
from openai import OpenAIError
from my_modules import view_sourcecode, modelName
import os
from langchain_community.callbacks import get_openai_callback
from ai_sidebar_content import AI_poet

# Function to interact with OpenAI API
def generate_text(api_key, input_text, language):
    try: 
        model_name = modelName()
         # Initialize your OpenAI instance using the provided API key
        llm = ChatOpenAI(openai_api_key=api_key,model_name=model_name )
        with get_openai_callback() as cb:
            generated_text = llm.invoke("Write me a poem about " + input_text + " in " + language + ", please!")
            st.write(cb)
        return generated_text
    except OpenAIError as e:
        st.warning("Incorrect API key provided or OpenAI API error.")
        st.warning(e)

def main():
    st.title('My AI Poet Assistant')

    # Get user input for OpenAI API key
    api_key = st.text_input("Please input your OpenAI API Key:", type="password")

    # Get user input for topic of the poem
    input_text = st.text_input('Throw a word for a poem topic, please!')
    st.write('The topic of the poem is ', input_text)

    # List of languages available for ChatGPT
    available_languages = ["English", "Korean", "Spanish", "French", "German", "Chinese", "Japanese"]

    # User-selected language
    selected_language = st.selectbox("Select a language:", available_languages)  

    # Button to trigger text generation
    if st.button("Creat a poem."):
        if api_key:
            with st.spinner('Wait for it...'):
                # When an API key is provided, display the generated text
                generated_text = generate_text(api_key, input_text, selected_language)
                st.write("Generated poem:")
                st.write(generated_text.content)
        else:
            st.warning("Please insert your OpenAI API key.")

    current_file_name = os.path.basename(__file__)
    view_sourcecode(current_file_name)

if __name__ == "__main__":
    main()

AI_poet()