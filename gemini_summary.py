import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def summarize_with_gemini(text: str) -> str:
    llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_GEMINI_MODEL_NAME"), google_api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = PromptTemplate(
        input_variables=["input"],
        template="Summarize this content:\n\n{input}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(text)
