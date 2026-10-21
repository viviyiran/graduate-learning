
import os
import json
import requests

# 1. API 配置
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("未找到 DEEPSEEK_API_KEY 环境变量")

url = "https://api.deepseek.com/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


# 2. 定义计算器工具
def calculate(num1, num2, operation):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2
    else:
        return "Error: Unsupported operation"


# 3. 定义工具描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算两个数字的加减乘除",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "第一个数字"
                    },
                    "num2": {
                        "type": "number",
                        "description": "第二个数字"
                    },
                    "operation": {
                        "type": "string",
                        "description": "运算方式",
                        "enum": ["+", "-", "*", "/"]
                    }
                },
                "required": ["num1", "num2", "operation"],
                "additionalProperties": False
            }
        }
    }
]


# 4. 初始化对话历史
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    }
]


# 5. 封装 API 请求
def call_deepseek():
    request_data = {
        "model": "deepseek-flash",
        "messages": messages,
        "stream": False,
        "tools": tools
    }

    response = requests.post(
        url,
        headers=headers,
        json=request_data,
        timeout=60
    )

    response.raise_for_status()
    return response.json()


# 6. 主循环
while True:
    question = input("\n请输入问题（输入 quit 退出）：").strip()

    if question.lower() == "quit":
        print("程序结束。")
        break

    if not question:
        continue

    # 保存本轮开始前的历史长度
    history_length = len(messages)

    # 保存用户问题
    messages.append({
        "role": "user",
        "content": question
    })

    try:
        # 最多允许连续 4 轮模型响应，避免无限工具调用
        for _ in range(4):

            # 请求 DeepSeek
            data = call_deepseek()
            message = data["choices"][0]["message"]

            # 7. 判断是否需要调用工具
            if message.get("tool_calls"):

                print("模型请求调用工具")

                # 先保存完整的 assistant 工具调用消息
                messages.append(message)

                # 逐个处理工具调用
                for tool_call in message["tool_calls"]:

                    function_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]

                    try:
                        args = json.loads(arguments)

                        # 8. 执行对应的 Python 函数
                        if function_name == "calculate":
                            result = calculate(
                                args["num1"],
                                args["num2"],
                                args["operation"]
                            )
                        else:
                            result = "Error: Unknown tool"

                    except (ValueError, TypeError, KeyError) as e:
                        result = f"Error: Invalid arguments: {e}"

                    print("工具执行结果：", result)

                    # 9. 保存工具执行结果
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": str(result)
                    })

                # 继续循环，将工具结果发回 DeepSeek
                continue

            # 10. 模型返回普通文本
            answer = message.get("content")

            if answer is None:
                raise ValueError("模型未返回文本或工具调用")

            print("AI:", answer)

            # 保存最终回答
            messages.append(message)
            break

        else:
            raise RuntimeError("连续工具调用次数超过限制")

    except (requests.RequestException, ValueError, KeyError,
            TypeError, RuntimeError) as e:

        print("本轮对话失败：", e)

        # 回退本轮未完成的消息，避免破坏历史记录
        del messages[history_length:]
