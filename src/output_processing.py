from pathlib import Path
import re

RESULTS_DIR: Path = Path("results")
RESULTS_FILE: Path = RESULTS_DIR / Path("results.txt")
results: list[str] = []

def get_result_files(results_dir: Path) -> list[Path]:
    return list(results_dir.glob("*"))

def get_filtered_content(file_path: Path, pattern: str) -> None:
    with open(file_path, "r") as f:
        content: str = f.read()
        for line in content.splitlines():
            if re.match(pattern, line.strip()):
                results.append(line+"\n")

def line_counter(file: Path) -> int:
    line_number: int = 0
    with open(file, "r") as f:
        for _ in f:
            line_number += 1
    return line_number

def log_results() -> None:
    with open(RESULTS_FILE, "w") as f:
        unique_results: list[str] = list(set(results))
        f.writelines(unique_results)

def run(domain) -> None:
    pattern: str = fr"^([a-zA-Z0-9-]+\.)+{re.escape(domain)}$"
    
    files_list: list[Path] = get_result_files(RESULTS_DIR)
    for file in files_list:
        get_filtered_content(file_path=file, pattern=pattern)
    
    log_results()
    
    line_number: int = line_counter(RESULTS_FILE)
    print(f"[+] {line_number} subdomains were found!")
