import json
import shutil

CONFIG_FILE: str = "config/config.json"
CUSTOM_DIR: str = "/opt/"

tools_local_paths: dict[str, str] = {}

def load_config(config_file: str) -> dict[str, str]:
    with open(config_file, "r") as conf:
        return json.load(conf)

def check_tool(tool: str, url: str) -> None:
    tool_path: str|None = shutil.which(tool)
    if not tool_path and CUSTOM_DIR:
        tool_path = shutil.which(tool, path=CUSTOM_DIR)
    
    if not tool_path:
        print(f"{tool} is missing... You can install it from {url}")
        return
    
    tools_local_paths[tool] = tool_path

def main() -> dict[str, str]:
    tools : dict[str, str] = load_config(CONFIG_FILE)
    
    for tool, url in tools.items():
        check_tool(tool, url)
    return tools_local_paths

if __name__ == "__main__":
    main()