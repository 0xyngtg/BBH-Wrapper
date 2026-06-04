import re
import json

from abc import ABC, abstractmethod

HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

CONFIG_FILE: str = "config/tools_args.json"

def load_config(config_file: str) -> dict[str, list[str]]:
    with open(config_file, "r") as conf:
        return json.load(conf)

class Tool(ABC):
    def __init__(self, path: str, args: list[str]):
        self.path = path
        self.args = args or []
    
    @abstractmethod
    def run(self) -> None:
        pass

class Findomain(Tool):
    def run(self) -> None:
        print(f"Running Findomain with {self.path} and {self.args}")

class Waymore(Tool):
    def run(self) -> None:
        print(f"Running Waymore with {self.path} and {self.args}")

class Sublister(Tool):
    def run(self) -> None:
        print(f"Running Sublist3r with {self.path} and {self.args}")

class GithubSubdomains(Tool):
    def run(self) -> None:
        print(f"Running GithubSubdomains with {self.path} and {self.args}")

class Shosubgo(Tool):
    def run(self) -> None:
        print(f"Running Shosubgo with {self.path} and {self.args}")

class Assetfinder(Tool):
    def run(self) -> None:
        print(f"Running Assetfinder with {self.path} and {self.args}")

def main(tools_local_path: dict[str, str]) -> None:
    arguments: dict[str, list[str]] = load_config(CONFIG_FILE)
    
    findomain: Findomain = Findomain(
        path=tools_local_path["findomain"],
        args=arguments["findomain"]
    )
    findomain.run()
    
    waymore: Waymore = Waymore(
        path=tools_local_path["findomain"],
        args=arguments["waymore"]
    )
    waymore.run()
    
    sublister: Sublister = Sublister(
        path=tools_local_path["sublist3r"],
        args=arguments["sublist3r"]
    )
    sublister.run()
    
    githubsubdomains: GithubSubdomains = GithubSubdomains(
        path=tools_local_path["github-subdomains"],
        args=arguments["github-subdomains"]
    )
    githubsubdomains.run()
    
    shosubgo: Shosubgo = Shosubgo(
        path=tools_local_path["shosubgo"],
        args=arguments["shosubgo"]
    )
    shosubgo.run()
    
    assetfinder: Assetfinder = Assetfinder(
        path=tools_local_path["assetfinder"],
        args=arguments["assetfinder"]
    )
    assetfinder.run()
