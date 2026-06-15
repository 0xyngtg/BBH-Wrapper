from bbh_wrapper import tool_checker
from bbh_wrapper import tool_runner
from bbh_wrapper import output_processing
from bbh_wrapper import probe_targets

TARGET: str = input("Target Domain > ")

def main() -> None:
    tools_local_paths: dict[str, str] = tool_checker.run()
    tool_runner.run(tools_local_paths=tools_local_paths, target=TARGET)
    output_processing.run(domain=TARGET)
    probe_targets.run()

if __name__ == "__main__":
    main()

