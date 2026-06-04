import tool_checker
import tool_runner

def main() -> None:
    tools_local_paths: dict[str, str] = tool_checker.main()

if __name__ == "__main__":
    main()

