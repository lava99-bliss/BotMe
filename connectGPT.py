
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import (SystemMessage,HumanMessage)


load_dotenv()

def emotionResponseGenerator(emotion_label1):
 openai_API_key = os.getenv("OPENAI_API_KEY")
 chat_model : ChatOpenAI = ChatOpenAI(openai_api_key=openai_API_key)

 sys_msg = SystemMessage(content=f"assume the user is feeeling {emotion_label1}.Now talk like a friend")
 human_msg= HumanMessage(content=f"you look like {emotion_label1} today. What made you look like that?")

 prediction_msg = chat_model.predict_messages([human_msg,sys_msg])
 return prediction_msg

def chatResponseGenerator(message):
  openai_API_key = os.getenv("OPENAI_API_KEY")
  chat_model : ChatOpenAI = ChatOpenAI(openai_api_key=openai_API_key)

  sys_msg = SystemMessage(content=f"{message}.Now talk like a friend")
  human_msg= HumanMessage(content=f"{message} ")

  prediction_msg = chat_model.predict_messages([human_msg,sys_msg])
  print(prediction_msg)
  return prediction_msg