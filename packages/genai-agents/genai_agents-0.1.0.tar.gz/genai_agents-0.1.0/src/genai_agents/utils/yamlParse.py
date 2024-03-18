import yaml
def getYamlAttribute(attrName):
    with open('src/genai_agents/config/agentConfig.yaml', 'r') as f:
     data = yaml.load(f, Loader=yaml.SafeLoader)
     attrValue=data.get(attrName)
     return attrValue
#print(getYamlAttribute('xorbotsCSVFileName'))