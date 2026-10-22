from .agent import SystemAgent, SysAgentState
import time


class Interface:
    def __init__(self):
        self.agent = SystemAgent
        self.timer = 60 * 60 # 1hr

    def active_worker(self):
        self.agent.invoke(SysAgentState(converstation=[]))

    def initalize(self):
        for _ in range(3):
            self.active_worker()
            time.sleep(self.timer)