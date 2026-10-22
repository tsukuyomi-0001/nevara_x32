from langchain_community.tools import DuckDuckGoSearchResults, ShellTool

ddgs_search = DuckDuckGoSearchResults()
shell_tools = ShellTool()
tools = [ddgs_search, ShellTool()]