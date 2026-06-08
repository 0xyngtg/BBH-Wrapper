import json
import tool_checker
import subprocess
from pathlib import Path
from dataclasses import dataclass

CONFIG_FILE: str = "config/tools_config.json"

TARGET: str = "domain.com"

type Arguments = dict[str, str]

@dataclass
class Tool:
    name: str
    path: Path
    arguments: Arguments
    
    def __post_init__(self):
        for arg, value in self.arguments.items():
            if value == "target":
                self.arguments[arg] = TARGET
            elif value == "output":
                self.arguments[arg] = f"{self.name}.out"
            elif value == "token":
                self.arguments[arg] = ""
    
    def run(self) -> subprocess.CompletedProcess:
        args_list = [self.path.name]
        for k, v in self.arguments.items():
            if v is None or v == "":
                continue
            args_list.append(k)
            args_list.append(v)
        try:
            print(f"[*] Running {self.name}...")
            result: subprocess.CompletedProcess = subprocess.run(args_list)
            return result
        except Exception as e:
            print(f"Error running {self.name}: {e}")
            raise

def load_config(config_file: str) -> dict[str, dict[str, str]]:
    with open(config_file, "r") as conf:
        return json.load(conf)

def run(tools_local_paths: dict[str, str]) -> None:
    tools_arguments: dict[str, Arguments] = load_config(CONFIG_FILE)
    
    for tool, arguments in tools_arguments.items():
        tool = Tool(
            name=tool,
            path=Path(tools_local_paths[tool]),
            arguments=arguments
        )
        tool.run()
