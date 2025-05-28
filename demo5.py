import csv
import os
from typing import Type, Optional
import requests
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.messages import HumanMessage
from langchain.tools.base import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import chat_agent_executor
from pydantic import BaseModel, Field
import langgraph

api_key = os.getenv('GLM_API_KEY')
os.environ['LANGCHAIN_TRACING'] = "true"
os.environ['LANGSMITH_ENDPOINT'] = "https://api.smith.langchain.com"
os.environ['LANGSMITH_PROJECT'] = "pr-shadowy-maybe-22"
os.environ['LANGCHAIN_PROJECT'] = "Tuo-Demo"


def find_code(csv_file_path, district_name) -> str:
    """
    File city/area code based on name.
    :param csv_file_path:
    :param district_name:
    :return:
    """
    district_map = {}
    with open(csv_file_path, mode = 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            district_code = row["district_id"].strip()
            district = row["district"].strip()
            if district not in district_map:
                district_map[district] = district_code
    return district_map.get(district_name, None)

class WeatherInputArgs(BaseModel):
    """
    the schema class of input
    """
    location: str= Field (..., description="to check the weather's location info")

class WeatherTool(BaseTool):
    """
    tool to check real-time weather
    """
    name = 'weather_tool'
    description = 'check current weather of any location'
    args_schema: Type[WeatherInputArgs] = WeatherInputArgs

    def _run(
            self,
            location: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """The function to automatically run when call the tool"""
        district_code = find_code('weather_district_id.csv', location)
        print(f'The location of {location} has a code: {district_code}')
        url = f'https://api.map.baidu.com/weather/v1/?district_id={district_code}&data_type=now&ak=qdkcGt9AtcYfIsArwnzGz4PS09feivdH'
        #I don't have a baidu ak. This AK is from the teacher.

        # Send the request
        response = requests.get(url)
        data = response.json()

        text = data["result"]["now"]['text']
        temp = data["result"]["now"]['temp']
        feels_like = data["result"]["now"]['feels_like']
        rh = data["result"]["now"]['rh']
        wind_dir = data["result"]["now"]['wind_dir']
        wind_class = data["result"]["now"]['wind_class']

        return f"Location: {location} Current weather: {text}, Temperature: {temp} °C, Feels like {feels_like} °C, Relative moisture: {rh} %，{wind_dir}:{wind_class}"

if __name__ == "__main__":
   print(find_code("./weather_district_id.csv", '石家庄'))

    # Create the model
   model = ChatOpenAI(
       model='glm-4-0520',
       api_key=api_key,
       base_url='https://open.bigmodel.cn/api/paas/v4/',
       temperature=0.6
   )

   tools = [WeatherTool()]

   agent_executor = chat_agent_executor.create_tool_calling_executor(model, tools)

   # resp = agent_executor.invoke({'messages': [HumanMessage(content='中国的首都是哪个城市？')]})
   # print(resp['messages'])

   resp2 = agent_executor.invoke({'messages': [HumanMessage(content='How\'s Beijing weather today?')]})
   # print(resp2['messages'])
   #
   # print(resp2['messages'][2].content)