from pydantic import BaseModel
from typing import Literal, Annotated

class SysAgentState(BaseModel):
    converstation: list
    system_logs: str = ''
    problem_statement: str = ''

class DecisionStucture(BaseModel):
    critical_state: Annotated[bool, "Is System in Critical State?"]
    need_for_repair: Annotated[bool, "Does System Truely need repair?"]
    necessity: Annotated[bool, "Can System work fine without repair?"]
    judgment: Annotated[bool, "Final Judgement, should repair happen on not?"]
    problem_statement: Annotated[str, "Give problem statement of what is the problem, what is the likely cause of the problem."]