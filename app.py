from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import datetime
import streamlit as st
from iching import iching


def predict(birthday, today):
    # birthday and today could be 19990526 and 20201023
    day = str(birthday) + str(today)
    dayStr = day.replace('-', '').replace('/', '')
    dayInt = int(dayStr)
    iching.ichingDate(dayInt)
    fixPred, changePred = iching.getPredict()
    # plotTransition(6, w = 15)
    guaNames = iching.ichingName(fixPred, changePred)
    fixText = iching.ichingText(fixPred)  #
    if changePred:
        changeText = iching.ichingText(changePred)  #
    else:
        changeText = None
    sepline1 = '\n                (O--__/\__--O)'
    sepline2 = '\n(-------------(O---- |__|----O)----------------)'
    sepline4 = '\n         (-------(O-/_--_\-O)-------)'
    sepline3 = '\n(-----------(O-----/-|__|-\------O)------------)'
    ben_gua = fixText + sepline1 + sepline2 + sepline3 + sepline4
    bian_gua = changeText
    return [guaNames, ben_gua, bian_gua]


def main():
    st.title("Cyber Future Teller")

    API_KEY = st.text_input("API Key")
    d = st.date_input("When's your birthday", value=None)
    user_question = st.text_input("Please enter your question:")

    if st.button("Answer") and user_question and d and API_KEY:
        with st.spinner("Processing..."):
            # init model
            llm = ChatOpenAI(openai_api_key=API_KEY, temperature=0.9, model_name="gpt-3.5-turbo-16k")
            # iching get today's gua
            today = int(datetime.datetime.now().strftime("%Y%m%d"))
            birthday = int(d.strftime("%Y%m%d"))
            predictions = predict(birthday, today)

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
