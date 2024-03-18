from  genai_agents.tools.tools_db import getDuckduckgoSearchResults
import logging
def search_string_in_list(my_list, target_string):
    """
    Search for a string in a list.

    Parameters:
    - my_list (list): The list to search through.
    - target_string (str): The string to search for.

    Returns:
    - list: A list of indices where the target string is found.
    """
    indices = []
    for index, item in enumerate(my_list):
        if item == target_string:
            indices.append(index)
    return indices


def getToolExecutionResults(agentName, role, goal, backstrory, task, capability, tools_list, llm_api):
    if (capability == "search_executor"):
        indices = search_string_in_list(tools_list, "duckduckgo-search")
        if indices:
             results = getDuckduckgoSearchResults(goal + task)
             print(f"executed duckduck search and results :{results}")
             return results
    else:
        logging.error("ERROR:tool_execution to be implemtned")
        print("ERROR in getToolExecutionResults\n")
        return "ERROR"
    
