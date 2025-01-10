import streamlit as st
from langchain_openai import ChatOpenAI
from openai import OpenAIError
from datetime import datetime
import os
from my_modules import view_sourcecode, modelName
from langchain_community.callbacks import get_openai_callback
from ai_sidebar_content import Todays_Counsel

# Function to interact with OpenAI API
def generate_text(api_key, birth_date, gender, language):
    try: 
        model_name = modelName()
        # Initialize your OpenAI instance using the provided API key
        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name)
        instruction = "사용자의 생년 월일 그리고 성별을 입력 받아 그 나이에 사용자가 생각하거나 행동하면 좋은 일들을 알려 주세요. 생년월일과 관계 되는 별자리와 꽃도 언급해 주세요. 동양에서 사용하는 띠도 알려 주세요. 그리고 용기를 내고 위안이 될 수 있는 말을 해 주세요. 현재까지 잘 살아 왔고 지금 나이에는 어떤 일들을 계획하고 행동하는게 좋은지 자세하게 알려 주세요. 올해는 2024년으로 설정하고 나이를 계산해 주세요. "
        query = instruction + ". " + birth_date + " 태어난 " + gender + "가 지금 생각하거나 행동해야 할 일은 무엇이 있을까요? 대답은 " + language + "로 해 주세요."
        # display_memory_buffer(query, llm)
        with get_openai_callback() as cb:
            generated_text = llm.invoke(query)
            st.write(cb)
        return generated_text
    except OpenAIError as e:
        st.warning("Incorrect API key provided or OpenAI API error. You can find your API key at https://platform.openai.com/account/api-keys.")

def main():
    st.title('Today\'s counsel ')

    # Get user input for OpenAI API key
    api_key = st.text_input("Please input your OpenAI API Key:", type="password")

    # Get the current year
    current_year = datetime.now().year   

    # Set year, month and date
    birth_date = st.date_input("Select your birth date", min_value=datetime(1900, 1, 1), max_value=datetime(current_year, 12, 31), format="MM/DD/YYYY")

    # Extract year, month, day from datetime.date
    year = str(birth_date.year)
    month = str(birth_date.month)
    day = str(birth_date.day)   

    birth_date_str = year + "년 " + month + "월 " + day + "일"    

    # Set gender
    gender = st.radio("Select your gender", ["Male", "Female"])

    # List of languages in which ChatGPT is available
    available_languages = ["English", "Korean", "Spanish", "French", "German", "Chinese", "Japanese"]

    # Language selected by user
    selected_language = st.selectbox("Select a language:", available_languages)  

    # Button to trigger text generation
    if st.button("Create a counsel."):
        if api_key:
            with st.spinner('Wait for it...'):    
                # When an API key is provided
                generated_text = generate_text(api_key, birth_date_str, gender, selected_language)
                st.write("Generated counsel:")
                st.write(generated_text.content)
        else:
            st.warning("Please insert your OpenAI API key.")

    current_file_name = os.path.basename(__file__)
    view_sourcecode(current_file_name)

if __name__ == "__main__":
    main()

Todays_Counsel()