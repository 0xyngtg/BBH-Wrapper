import json
import subprocess
from pathlib import Path
from dataclasses import dataclass

type Arguments = dict[str, str]

CONFIG_FILE: str = "config/config.json"
TOKENS_FILE: str = "config/tokens.json"
RESULTS_DIR: str = "results"

@dataclass
class Tool:
    target: str
    name: str
    path: Path
    arguments: Arguments
    _token: str|None
    
    def __post_init__(self) -> None:
        for arg, value in self.arguments.items():
            if value == "target":
                self.arguments[arg] = self.target
            elif value == "output":
                self.arguments[arg] = f"{RESULTS_DIR}/{self.name}.out"
            elif value == "token":
                self.arguments[arg] = f"{self._token}"
    
    def run(self) -> None:
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
            result: subprocess.CompletedProcess = subprocess.run(args_list, capture_output=True, text=True)
            
            if ["-f", "-o", "-oU"] not in args_list:
                with open(f"{RESULTS_DIR}/{self.name}.out", "w") as f:
                    f.write(result.stdout)
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

def run(tools_local_paths: dict[str, str], target: str) -> None:
    tools_arguments: dict[str, Arguments] = load_config(CONFIG_FILE)
    tokens: dict[str, str] = load_tokens(TOKENS_FILE)
    
    for tool, arguments in tools_arguments.items():
        if arguments == {}:
            continue
        elif "token" in arguments.values():
            token: str|None = tokens.get(tool)
            if token is None or token == "":
                print(f"[-] WARNING: Skipping {tool} because no token was supplied! Check \"config/tokens.json\"...")
                continue
        else:
            token = None
        
        try:
            path: Path = Path(tools_local_paths[tool])
        except KeyError:
            print(f"[-] ERROR: {tool} not found!")
            continue
        
        tool = Tool(
            target=target,
            name=tool,
            path=path,
            arguments=arguments,
            _token=token
        )
        
        tool.run()
