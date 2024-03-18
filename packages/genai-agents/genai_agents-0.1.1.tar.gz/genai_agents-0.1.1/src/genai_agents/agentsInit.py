import sys
import threading
import logging

from genai_agents.AIAgent import (
    createAndsendMessageProfTrigger,
    getGMapper,
    main_condition,
    setGMapper,
    setGTimerList,
    waitonConditionMain,
)
from genai_agents.MessageBroker import NameIndexMapper


def agentThreadsStart(agentObjectList):
    mapper = getGMapper()
    for obj in agentObjectList:
        obj.start_agent(mapper)


def agentInitSystem(agent_list):
    logging.debug("kick-off of the program")
    mapper = NameIndexMapper()
    timerPool = mapper.timerPool
    setGTimerList(timerPool)

    for agent in agent_list:
        mapper.add_mapping(agent)

    setGMapper(mapper)
    timer_thread = threading.Thread(target=timerPool.run)
    timer_thread.daemon = True
    logging.info("timer demon started")
    timer_thread.start()

def triggerAgent(agent_list, godTimerDuration):
    msg1 = "HGI sending trigger message to start the execution"
    mapper = getGMapper()
    for agent in agent_list:
        createAndsendMessageProfTrigger("profAgent", agent, msg1, mapper)
    waitonConditionMain(main_condition, godTimerDuration)
    logging.info("final exit")
    sys.exit()

def kickOffGenAIAgents2(AgentObjects, triggerAgentObjectsList): 
    agent_list=[]

    #extract agent names
    for agentObj in AgentObjects:
        agent_list.append(agentObj.agentName)
    agentInitSystem(agent_list=agent_list)
    print(agent_list)
    agentThreadsStart(agentObjectList=AgentObjects)

    #extract - trigger agent list
    triggerAgentList=[]
    for triggerObj in triggerAgentObjectsList:
        triggerAgentList.append(triggerObj.agentName)
    print(triggerAgentList)
    triggerAgent(triggerAgentList, godTimerDuration=10000)

def searchItemInList(DynamicAgentObjectsList, target):
    for  item in DynamicAgentObjectsList:
        if item.agentName == target.agentName:
            # print("Found")
            return True       
    return False
    
def kickOffGenAIAgents(AgentObjects, triggerAgentObjectsList, DynamicAgentObjectsList=[]): 
    agent_list=[]
    #extract agent names
    for agentObj in AgentObjects:
        agent_list.append(agentObj.agentName)
    agentInitSystem(agent_list=agent_list)
    print(agent_list)
    if(not DynamicAgentObjectsList):
        agentThreadsStart(agentObjectList=AgentObjects)
    else:
        for item in AgentObjects:
            if(not searchItemInList(DynamicAgentObjectsList, item)):
                # print("Not Found")
                mapper = getGMapper()
                item.start_agent(mapper)
    #extract - trigger agent list
    triggerAgentList=[]
    for triggerObj in triggerAgentObjectsList:
        triggerAgentList.append(triggerObj.agentName)
    print(triggerAgentList)
    triggerAgent(triggerAgentList, godTimerDuration=10000)