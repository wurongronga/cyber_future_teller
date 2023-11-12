from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import datetime
import streamlit as st
from iching import iching

def main():
    load_dotenv()  # take environment variables from .env.

    st.title("Cyber Future Teller")

    # upload api key
    with st.sidebar:
        st.subheader("enter your own API key")
        api_key = st.text_input("API Key")
        if st.button("Submit") and api_key:
            with st.spinner("Saving..."):
                API_KEY = api_key
                st.write("recived API key")

    llm = ChatOpenAI(openai_api_key=API_KEY, temperature=0.9, model_name="gpt-3.5-turbo-16k")
    d = st.date_input("When's your birthday", value=None)
    user_question = st.text_input("Please enter your question:")

    if st.button("Answer") and user_question and d and llm:
        with st.spinner("Processing..."):
            # iching get today's gua
            today = int(datetime.datetime.now().strftime("%Y%m%d"))
            birthday = int(str(d.year) + str(d.month) + str(d.day))
            predictions = iching.predict(birthday, today)
            # pass gua into model
            template = f"""作为一个易经解卦大师，你将基于推演起卦的结果回答客人的问题。
                                推演起卦的结果包括卦名、本卦和变卦，目前的卦相为：
                                卦名 - {predictions[0]}
                                本卦 - {predictions[1]}
                                变卦 - {predictions[2]}
                                客人将会输入他的问题。
                           """
            chat_prompt = ChatPromptTemplate.from_messages([
                ("system", template),
                ("human", user_question),
            ])
            chain = chat_prompt | llm
            result = chain.invoke({"text": "colors"})
            st.write(result.content)

if __name__ == "__main__":
    main()