import json
import subprocess
from pathlib import Path
from dataclasses import dataclass

type Arguments = dict[str, str]

CONFIG_FILE: str = "config/config.json"
TOKENS_FILE: str = "config/tokens.json"
TARGET: str = input("Target Domain > ")

@dataclass
class Tool:
    name: str
    path: Path
    arguments: Arguments
    token: str|None
    
    def __post_init__(self):
        for arg, value in self.arguments.items():
            if value == "target":
                self.arguments[arg] = TARGET
            elif value == "output":
                self.arguments[arg] = f"{self.name}.out"
            elif value == "token":
                self.arguments[arg] = f"{self.token}"
    
    def run(self) -> subprocess.CompletedProcess:
        args_list = [self.path.name]
        for k, v in self.arguments.items():
            if v is None or v == "":
                args_list.append(k)
                continue
            if k == "":
                args_list.append(v)
            else:
                args_list.append(k)
                args_list.append(v)
        try:
            print(f"[*] Running {self.name}...")
            print(args_list)
            #result: subprocess.CompletedProcess = subprocess.run(args_list)
            #return result
        except Exception as e:
            print(f"Error running {self.name}: {e}")
            raise

def load_config(config_file: str) -> dict[str, dict[str, str]]:
    with open(config_file, "r") as conf:
        config: dict = json.load(conf)
        tools_args: dict[str, dict[str, str]] = config.get("tools_args")
        return tools_args

def load_tokens(token_file: str) -> dict[str, str]:
    with open(token_file, "r") as t:
        tokens: dict[str, str] = json.load(t)
        return tokens

def run(tools_local_paths: dict[str, str]) -> None:
    tools_arguments: dict[str, Arguments] = load_config(CONFIG_FILE)
    tokens: dict[str, str] = load_tokens(TOKENS_FILE)
    
    for tool, arguments in tools_arguments.items():
        if tokens.get(tool):
            token: str|None = tokens.get(tool)
        else:
            token = None
        
        tool = Tool(
            name=tool,
            path=Path(tools_local_paths[tool]),
            arguments=arguments,
            token=token
        )
        
        tool.run()

