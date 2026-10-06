from dotenv import load_dotenv
import os 
from langchain_groq import ChatGroq
llm = ChatGroq(model = "openai/gpt-oss-20b")

res = llm.invoke("Hello ! ")
print(res.content)




load_dotenv()

#State - GLoabal state to pass the data b/w all nodes 

from pydeatic import BaseModel 
class UserState(BaseModel):
    name: str = ""
    email:str= ""
    age:int =0

state = UserState(name ="vivek", email="vivekit2001@gmail.com",age = 21)

##########2 Bilding the Graph using Langgraph ####################################

from Langgraph.Graph import StateGraph , START , END 
from pydentic import BaseModel

class MyState(BaseModel):
    messages : str = ""

def greet(state:MyState):
    "i am greet node..."
     print(state.messages)
     return state

graph = StateGraph(MyState)
graph.add_node("greet" ,greet)

graph.add_edge(START,"greet")
graph.add_edge("greet",END)


final_graph = graph.compile()


res = final_graph.invoke({"messages":"hello ...."})



###Multi Node Graph 
 from random import randint 
 
# start --> score -->commenter ---> end

class ReviewState(BaseModel):
    text : str =""
    score: int = 0
    comment: str = ""

def score(state:ReviewState):
    state.score = rendint(1,10)
    return state

def commenter(state:ReviewState):
    if state.score >5:
        state.comment ="welldone"
     else:
        stste.comment = "Need Improvement"

     return state

graph = StateGraph(ReviewState)
graph.add_node("score", score)
graph.add_node("commenter",commenter)

graph.add_edge(START,"score")
graph.add_edge("score","commenter")
graph.add_edge("commenter",END)


final_graph = graph.compile()

res = final_graph.invoke({})
print(res)














