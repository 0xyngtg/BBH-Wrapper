import src.bbh_wrapper.tool_checker as tool_checker
import src.bbh_wrapper.tool_runner as tool_runner
import src.bbh_wrapper.output_processing as output_processing
import src.bbh_wrapper.probe_targets as probe_targets

TARGET: str = input("Target Domain > ")

def main() -> None:
    tools_local_paths: dict[str, str] = tool_checker.run()
    tool_runner.run(tools_local_paths=tools_local_paths, target=TARGET)
    output_processing.run(domain=TARGET)
    probe_targets.run()

if __name__ == "__main__":
    main()

