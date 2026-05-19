import json
import time
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Message:
    role: str
    content: str
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class ToolResult:
    tool_name: str
    success: bool
    result: Any
    error: Optional[str] = None


class BaseTool(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_parameters(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        pass


class CalculatorTool(BaseTool):
    def get_name(self) -> str:
        return "calculator"
    
    def get_description(self) -> str:
        return "用于执行数学计算，支持加减乘除和幂运算"
    
    def get_parameters(self) -> List[Dict[str, Any]]:
        return [
            {"name": "expression", "type": "string", "description": "数学表达式，如 '2 + 3 * 4'"}
        ]
    
    def execute(self, **kwargs) -> ToolResult:
        expression = kwargs.get("expression", "")
        try:
            result = eval(expression)
            return ToolResult(tool_name=self.get_name(), success=True, result=result)
        except Exception as e:
            return ToolResult(tool_name=self.get_name(), success=False, result=None, error=str(e))


class WeatherTool(BaseTool):
    def get_name(self) -> str:
        return "get_weather"
    
    def get_description(self) -> str:
        return "获取指定城市的天气信息"
    
    def get_parameters(self) -> List[Dict[str, Any]]:
        return [
            {"name": "city", "type": "string", "description": "城市名称"}
        ]
    
    def execute(self, **kwargs) -> ToolResult:
        city = kwargs.get("city", "")
        mock_weather = {
            "北京": {"temperature": 25, "condition": "晴", "humidity": 45},
            "上海": {"temperature": 28, "condition": "多云", "humidity": 60},
            "广州": {"temperature": 32, "condition": "雷阵雨", "humidity": 85},
            "深圳": {"temperature": 30, "condition": "阴", "humidity": 70}
        }
        if city in mock_weather:
            return ToolResult(tool_name=self.get_name(), success=True, result=mock_weather[city])
        else:
            return ToolResult(tool_name=self.get_name(), success=False, result=None, error=f"未找到城市 {city} 的天气信息")


class MemorySystem:
    def __init__(self, max_messages: int = 100):
        self.messages: List[Message] = []
        self.max_messages = max_messages
    
    def add_message(self, message: Message):
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_history(self, limit: int = 20) -> List[Message]:
        return self.messages[-limit:]
    
    def get_summary(self) -> str:
        if not self.messages:
            return "无历史对话记录"
        recent = self.get_history(5)
        summary = "最近对话摘要：\n"
        for msg in recent:
            summary += f"{msg.role}: {msg.content}\n"
        return summary
    
    def clear(self):
        self.messages = []


class Agent:
    def __init__(self, name: str = "SmartAgent"):
        self.name = name
        self.memory = MemorySystem()
        self.tools: List[BaseTool] = [CalculatorTool(), WeatherTool()]
        self.thought_process: List[str] = []
    
    def _format_tool_list(self) -> str:
        tools_info = []
        for tool in self.tools:
            params = ", ".join([f"{p['name']} ({p['type']})" for p in tool.get_parameters()])
            tools_info.append(f"- {tool.get_name()}: {tool.get_description()} (参数: {params})")
        return "\n".join(tools_info)
    
    def _extract_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        if "tool_name" in text:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                if start != -1 and end != -1:
                    return json.loads(text[start:end])
            except Exception as e:
                self.thought_process.append(f"解析工具调用失败: {e}")
        return None
    
    def _generate_response(self, messages: List[Message]) -> str:
        history = "\n".join([f"{m.role}: {m.content}" for m in messages])
        prompt = f"""你是一个智能助手 {self.name}。
可用工具：
{self._format_tool_list()}

如果需要使用工具，请以 JSON 格式输出 tool_call，例如：
{{"tool_name": "calculator", "parameters": {{"expression": "2 + 3"}}}}

如果不需要工具，直接回答用户问题。

历史对话：
{history}

当前问题：{messages[-1].content if messages else ""}

你的回答："""
        
        mock_response = self._mock_llm_response(messages)
        return mock_response
    
    def _mock_llm_response(self, messages: List[Message]) -> str:
        if not messages:
            return "你好！我是智能助手，有什么可以帮助你的？"
        
        last_msg = messages[-1].content.lower()
        
        if any(op in last_msg for op in ["加", "减", "乘", "除", "计算", "等于", "+"]):
            expression = ""
            for char in last_msg:
                if char in "0123456789+-*/.^ ":
                    expression += char
            if expression.strip():
                return f'{{"tool_name": "calculator", "parameters": {{"expression": "{expression.strip()}"}}}}'
        
        if any(w in last_msg for w in ["天气", "温度", "下雨", "晴天"]):
            cities = ["北京", "上海", "广州", "深圳"]
            for city in cities:
                if city in last_msg:
                    return f'{{"tool_name": "get_weather", "parameters": {{"city": "{city}"}}}}'
        
        return self._generate_direct_response(last_msg)
    
    def _generate_direct_response(self, question: str) -> str:
        responses = {
            "你好": "你好！很高兴为你服务。",
            "嗨": "嗨！有什么需要帮助的吗？",
            "谢谢": "不客气！有问题随时找我。",
            "再见": "再见！祝你有美好的一天。",
            "你是谁": f"我是 {self.name}，一个智能助手。",
            "你能做什么": f"我可以帮助你回答问题、进行数学计算、查询天气等。\n可用工具：\n{self._format_tool_list()}"
        }
        
        for key, response in responses.items():
            if key in question:
                return response
        
        return f"我收到了你的问题：'{question}'。这是一个直接回答。如果你需要计算或查询天气，请告诉我。"
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> ToolResult:
        for tool in self.tools:
            if tool.get_name() == tool_name:
                return tool.execute(**parameters)
        return ToolResult(tool_name=tool_name, success=False, result=None, error="工具不存在")
    
    def chat(self, user_input: str) -> str:
        user_message = Message(role="user", content=user_input)
        self.memory.add_message(user_message)
        
        self.thought_process.append(f"用户输入: {user_input}")
        
        response = self._generate_response(self.memory.get_history())
        self.thought_process.append(f"生成响应: {response}")
        
        tool_call = self._extract_tool_call(response)
        
        if tool_call:
            tool_name = tool_call.get("tool_name")
            parameters = tool_call.get("parameters", {})
            
            self.thought_process.append(f"调用工具: {tool_name}, 参数: {parameters}")
            
            result = self._execute_tool(tool_name, parameters)
            self.thought_process.append(f"工具执行结果: {result}")
            
            if result.success:
                result_msg = Message(role="tool", content=f"工具执行成功: {result.result}")
                self.memory.add_message(result_msg)
                
                final_response = self._summarize_tool_result(tool_name, result.result)
            else:
                result_msg = Message(role="tool", content=f"工具执行失败: {result.error}")
                self.memory.add_message(result_msg)
                final_response = f"工具执行失败: {result.error}"
        else:
            final_response = response
        
        agent_message = Message(role="assistant", content=final_response)
        self.memory.add_message(agent_message)
        
        return final_response
    
    def _summarize_tool_result(self, tool_name: str, result: Any) -> str:
        if tool_name == "calculator":
            return f"计算结果：{result}"
        elif tool_name == "get_weather":
            return f"天气信息 - 温度: {result['temperature']}°C, 天气状况: {result['condition']}, 湿度: {result['humidity']}%"
        else:
            return f"工具执行结果：{result}"


def main():
    print("欢迎使用智能助手！")
    print("我可以帮助你进行数学计算、查询天气等。")
    print("输入 'exit' 或 'quit' 退出对话。\n")
    
    agent = Agent(name="智能小助手")
    
    while True:
        user_input = input("你: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("智能小助手: 再见！祝你有美好的一天。")
            break
        
        response = agent.chat(user_input)
        print(f"智能小助手: {response}\n")


if __name__ == "__main__":
    main()