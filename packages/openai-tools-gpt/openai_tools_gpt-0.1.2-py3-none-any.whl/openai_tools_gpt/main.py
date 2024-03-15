"""AutoGTP Module"""

import os
import json
from typing import Callable, Iterator, AsyncIterator, Any
from json import JSONDecodeError

from openai import AsyncOpenAI, OpenAI
from retry import retry


class ToolsGPT:
    """
    A class for regular and streaming support responses using OpenAI's GPT models.
    Provides an async context manager to stream responses with the OpenAI models.

    Attributes:
        - model (str): The OpenAI model to use.
        - with_memory (bool): if the model is meant to have memory
        - memory (list): Container for conversation history.
        - tools_schema (list[dict]|None): Optional List of tools the model may call.
        - tools (dict[str, Callable]|None): Optional tools functions to get model response
          when tools_schema enable.
        - tool_choice (str|None): When tools_schema and tools enable, this is for telling the
           model which tool to use by default or automatically.
        - temperature (int): Sampling temperature for model responses.
        - response_format (str): Format for model responses.
        - debug (bool): if intermediate steps wants to be seen

    Methods:
        - function_calling: Parses the AI response to get the function name and arguments.
        Looks up the function object in the tools dict and calls it,
        passing the arguments.

        Returns the function response and name as a tuple.

        - stream: retrieve a synchronous answer from OpenAI API with tool function injection.

        Get OpenAI streaming response. Parses stream response to extract
        tool function calls. Calls tool functions with provided arguments.
        Injects tool response into conversation history. Retrieves final stream
        response. Yields response text chunks.

        Calls as many tools as needed for given a response.

        If not tools necessary, yields regular response text chunks.

        - astream: The same as the stream method but with asynchronous support

        - invoke: retrieve a synchronous regular answer from OpenAI API.

        Get OpenAI streaming response. get too functions to call. Calls
        tool functions with provided arguments.
        Injects tool response into conversation history. Retrieves final
        response.

        No streaming suported.

        Calls as many tools as needed for given a response.

        If not tools necessary, returns regular response.

    Example:
        - No tools:
            >>> instance = StreamingAutoGPT()
            >>> instance.stream(query) | instance.astream(query) | instance.invoque
        - Tools:
            >>> instance = StreamingAutoGPT(tools_schema=tools_schema, tools=tools, tool_choice=tool_choice)
            >>> instance.stream(query) | instance.astream(query) | instance.invoque

        In both cases the Class handle the response properly, whether you use tools or not
    """

    def __init__(
        self,
        model="gpt-3.5-turbo",
        with_memory: bool = False,
        memory: None | list = None,
        tools_schema: None | list = None,
        tools: None | dict[str, Callable] = None,
        tool_choice: None | str = None,
        temperature: int = 0,
        response_format: str = "text",
        debug: bool = False,
    ) -> None:
        """
        Initialize the StreamingAutoGPT instance.

        Parameters:
            - model (str): The OpenAI model to use, default "gpt-3.5-turbo".
            - with_memory (bool): if the model is meant to have memory.
              Possibles values are True, False
            - memory (list): Initial prompt memory to seed the model with.
            - tools_schema (list[dict]|None): Optional List of tools the model may call.
              A single tool squema follows this structure (JSON Schema):
                  {
                        "type": "function",
                        "function": {
                            "name": "function_name",
                            "description": "describe what is the function goal",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "property_a": {
                                        "type": "string",
                                        "description": "property description",
                                    },
                                    "property_b": {
                                        "type": "number",
                                        "description": "property description",
                                        "enum": [1, 2, 3, 4], # To indicate which values are allow
                                    },
                                    "property_c": {
                                        "type": "string",
                                        "description": "property description",
                                        "enum": ["a", "b"],
                                    },
                                },
                                "required": ["property_a", "property_c"], # To indicate which parameters must be retrieved
                            },
                        },
                    }
            - tools (dict[str, Callable]|None): Optional tools functions to inject into the model.
              Example value is {"tool_name": tool_name}
            - tool_choice (str|None): When tools_schema and tools enable, this is for telling the
              model which tool to use by default or automatically.
              Possible values are 'auto', 'none', {"type": "function", "function": {"name": "function_name"}}
            - temperature (int): Sampling temperature for model responses, default 0.
              values from 0 to 1
            - response_format (str): Format for model responses, default "text".
              Possible values are "text", "json_object" must also specified in the template that you want a json response.
            - debug (bool): intermediate steps should be seen.
              Possible values are True, False
        """

        self.async_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.sync_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        self.model = model
        self.with_memory = with_memory
        self.memory = memory if memory else []
        self.tools_schema = tools_schema
        self.tools = tools
        self.tool_choice = tool_choice
        self.temperature = temperature
        self.response_format = (
            {"type": "text"} if response_format == "text" else {"type": "json_object"}
        )
        self.debug: bool = debug

    def function_calling(self, ai_response: dict[str, Any]) -> tuple:
        """
        Function to call a tool function from the AI response.

        Parses the AI response to get the function name and arguments.
        Looks up the function object in the tools dict and calls it,
        passing the arguments.

        Returns the function response and name as a tuple.

        Parameters:
            - ai_response (dict): object with the tool information (name and parameters)

        Returns:
            - Tuple: the function response and the function name
        """

        # Getting function data
        function_name: str = ai_response["function"]["name"]
        function_object: Callable = self.tools[function_name]
        function_args: dict = json.loads(ai_response["function"]["arguments"])

        # Calling the function
        function_response: str = function_object(**function_args)

        try:
            if self.debug:
                print(
                    " " * 4,
                    "*",
                    function_name.upper(),
                    f"\n{' '*8}Arguments:\n",
                    json.dumps(function_args, indent=4),
                    f"\n{' '*8}Response:\n",
                    json.dumps(json.loads(function_response), indent=4),
                    end="\n\n",
                )
        except JSONDecodeError:
            print(
                " " * 4,
                "*",
                function_name.upper(),
                f"\n{' '*8}Arguments:\n",
                json.dumps(function_args, indent=4),
                f"\n{' '*8}Response:\n",
                function_response,
                end="\n\n",
            )

        return function_response, function_name

    # run function_calling_LLM
    @retry(delay=4, tries=2)
    def stream(self, query: str) -> Iterator[str]:
        """
        Function to retrieve a synchronous answer from OpenAI API with tool function injection.

        Get OpenAI streaming response. Parses stream response to extract
        tool function calls. Calls tool functions with provided arguments.
        Injects tool response into conversation history. Retrieves final stream
        response. Yields response text chunks.

        Calls as many tools as needed for given a response.

        If not tools necessary, yields regular response text chunks.

        Parameters:
            - query (str): user input

        Yields:
            - str: a piece of chunk text
        """

        self.memory.append({"role": "user", "content": query})

        response = self.sync_client.chat.completions.create(
            model=self.model,
            messages=self.memory,
            temperature=self.temperature,
            tools=self.tools_schema,
            tool_choice=self.tool_choice,
            stream=True,
        )

        recovered_pieces = {"content": None, "role": "assistant", "tool_calls": {}}
        answer = ""

        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content is None:
                if delta.tool_calls:
                    piece = delta.tool_calls[0]
                    recovered_pieces["tool_calls"][piece.index] = recovered_pieces[
                        "tool_calls"
                    ].get(
                        piece.index,
                        {
                            "id": None,
                            "function": {"arguments": "", "name": ""},
                            "type": "function",
                        },
                    )
                    if piece.id:
                        recovered_pieces["tool_calls"][piece.index]["id"] = piece.id
                    if piece.function.name:
                        recovered_pieces["tool_calls"][piece.index]["function"][
                            "name"
                        ] = piece.function.name
                    recovered_pieces["tool_calls"][piece.index]["function"][
                        "arguments"
                    ] += piece.function.arguments

            else:
                answer += delta.content
                yield delta.content

        tool_calls = recovered_pieces["tool_calls"]

        if self.debug:
            if tool_calls:
                print("USING TOOLS:")
                print(f"{' '*2}TOOLS CALLED:\n")
            else:
                print("\n\nNOT TOOLS USAGE\n")

        if tool_calls:
            recovered_pieces["tool_calls"] = list(tool_calls.values())
            for index, tool_call in enumerate(tool_calls.values()):
                function_response, function_name = self.function_calling(tool_call)
                if index == 0:
                    self.memory.append(recovered_pieces)
                self.memory.append(
                    {
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = self.sync_client.chat.completions.create(
                model=self.model,
                messages=self.memory,
                temperature=self.temperature,
                response_format=self.response_format,
                stream=True,
            )

            if not self.with_memory:
                for _ in range(len(tool_calls) + 1):
                    self.memory.pop()

            if self.debug == True:
                print("\nANSWER:")

            for chunk in second_response:
                chunk = chunk.choices[0].delta.content
                if chunk:
                    answer += chunk
                    yield chunk

        if self.with_memory:
            self.memory.append({"role": "assistant", "content": answer})
        else:
            self.memory.pop()

    @retry(delay=4, tries=2)
    async def astream(self, query: str) -> AsyncIterator[str]:
        """
        Function to retrieve an asynchronous answer from OpenAI API with tool function injection.

        Get OpenAI streaming response. Parses stream response to extract
        tool function calls. Calls tool functions with provided arguments.
        Injects tool response into conversation history. Retrieves final stream
        response. Yields response text chunks.

        Calls as many tools as needed for given a response.

        If not tools necessary, yields regular response text chunks.

        Parameters:
            - query (str): user input

        Yields:
            - str: a piece of chunk text
        """

        self.memory.append({"role": "user", "content": query})

        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=self.memory,
            tools=self.tools_schema,
            tool_choice=self.tool_choice,
            stream=True,
        )

        recovered_pieces = {"content": None, "role": "assistant", "tool_calls": {}}
        answer = ""

        async for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content is None:
                if delta.tool_calls:
                    piece = delta.tool_calls[0]
                    recovered_pieces["tool_calls"][piece.index] = recovered_pieces[
                        "tool_calls"
                    ].get(
                        piece.index,
                        {
                            "id": None,
                            "function": {"arguments": "", "name": ""},
                            "type": "function",
                        },
                    )
                    if piece.id:
                        recovered_pieces["tool_calls"][piece.index]["id"] = piece.id
                    if piece.function.name:
                        recovered_pieces["tool_calls"][piece.index]["function"][
                            "name"
                        ] = piece.function.name
                    recovered_pieces["tool_calls"][piece.index]["function"][
                        "arguments"
                    ] += piece.function.arguments

            else:
                answer += delta.content
                yield delta.content

        tool_calls = recovered_pieces["tool_calls"]

        if self.debug:
            if tool_calls:
                print("USING TOOLS:")
                print(f"{' '*2}TOOLS CALLED:\n")
            else:
                print("\n\nNOT TOOLS USAGE\n")

        if tool_calls:
            recovered_pieces["tool_calls"] = list(tool_calls.values())
            for index, tool_call in enumerate(tool_calls.values()):
                function_response, function_name = self.function_calling(tool_call)
                if index == 0:
                    self.memory.append(recovered_pieces)
                self.memory.append(
                    {
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = await self.async_client.chat.completions.create(
                model=self.model, messages=self.memory, stream=True
            )

            if not self.with_memory:
                for _ in range(len(tool_calls) + 1):
                    self.memory.pop()

            if self.debug:
                print("\n\nANSWER:")

            async for chunk in second_response:
                chunk = chunk.choices[0].delta.content
                if chunk:
                    answer += chunk
                    yield chunk

        if self.with_memory:
            self.memory.append({"role": "assistant", "content": answer})
        else:
            self.memory.pop()

    def invoke(self, query: str) -> str:
        """
        Function to retrieve a synchronous regular answer from OpenAI API.

        Get OpenAI streaming response. get too functions to call. Calls
        tool functions with provided arguments.
        Injects tool response into conversation history. Retrieves final
        response.

        No streaming suported.

        Calls as many tools as needed for given a response.

        If not tools necessary, returns regular response.

        Parameters:
            - query (str): user input

        Returns:
            - str: model response
        """
        self.memory.append({"role": "user", "content": query})
        answer: str

        response = self.sync_client.chat.completions.create(
            model=self.model,
            messages=self.memory,
            temperature=self.temperature,
            tools=self.tools_schema,
            tool_choice=self.tool_choice,
        )

        tool_calls = response.choices[0].message.tool_calls

        if self.debug:
            if tool_calls:
                print("USING TOOLS:")
                print(f"{' '*2}TOOLS CALLED:\n")
            else:
                print("\n\nNOT TOOLS USAGE\n")

        if tool_calls:
            self.memory.append(
                {"role": "assistant", "content": None, "tool_calls": tool_calls}
            )

            for tool in tool_calls:
                function_name = tool.function.name
                function_object = self.tools[function_name]
                function_args = json.loads(tool.function.arguments)
                function_response = function_object(**function_args)
                self.memory.append(
                    {
                        "role": "tool",
                        "content": function_response,
                        "tool_call_id": tool.id,
                    }
                )

                if self.debug:
                    print(
                        " " * 4,
                        "*",
                        function_name.upper(),
                        f"\n{' '*8}Arguments:\n",
                        json.dumps(function_args, indent=4),
                        f"\n{' '*8}Response:\n",
                        json.dumps(json.loads(function_response), indent=4),
                        end="\n\n",
                    )

            second_response = self.sync_client.chat.completions.create(
                model=self.model,
                messages=self.memory,
                temperature=self.temperature,
                response_format=self.response_format,
            )

            if not self.with_memory:
                for _ in range(len(tool_calls) + 1):
                    self.memory.pop()

            answer = second_response.choices[0].message.content
        else:
            answer = response.choices[0].message.content

        if self.with_memory:
            self.memory.append({"role": "assistant", "content": answer})
        else:
            self.memory.pop()

        if self.debug:
            print(f"\nANSWER:")

        return answer
