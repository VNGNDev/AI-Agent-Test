import os
import sys
import json
from functions.call_function import available_functions, call_function
from openai import OpenAI
import argparse
from dotenv import load_dotenv
from prompts import system_prompt

load_dotenv()

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

api_key = os.environ.get("OPENROUTER_API_KEY")
messages: list[dict] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
]

client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
)

def response_chat():
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
    )
    return response

def main():

    for _ in range(20):
        response = response_chat()
        message = response.choices[0].message
        messages.append(message)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens if response.usage is not None else ""}")
            print(f"Response tokens: {response.usage.completion_tokens if response.usage is not None else ""}")
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call)
                messages.append(result_message)
                if not result_message["content"]:
                    raise Exception('No content in the result')

                print(f"-> {result_message['content']}")
                #function_args = json.loads(tool_call.function.arguments or "{}")
                #print(f"Calling function: {tool_call.function.name}({function_args})")
        else:
            print(response.choices[0].message.content)
            sys.exit(0)

    sys.exit(1)


if __name__ == "__main__":
    main()
