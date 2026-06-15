import requests
from threading import Thread, Lock
from pathlib import Path

LOCK = Lock()
RESULTS_DIR: Path = Path("results")
RESULTS_FILE: Path = RESULTS_DIR / Path("results.txt")
ALIVE_HOSTS_FILE: Path = RESULTS_DIR / Path("alive_hosts.txt")
alive_hosts_list: list[str] = []

HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (X11; Linux; rv:74.0) Gecko/20100101 Firefox/74.0"
}

def open_subs_file(file: Path) -> list[str]:
    targets: list[str] = []
    schemas: list[str] = ["http://", "https://"]
    with open(file, "r") as f:
        for line in f.readlines():
            for schema in schemas:
                targets.append(schema+line.strip())
    return targets

def worker(url: str) -> None:
    try:
        requests.Response = requests.get(url=url, headers=HEADERS, timeout=5)
        with LOCK:
            alive_hosts_list.append(url)
    except requests.RequestException as e:
        pass

def log_results() -> None:
    with open(ALIVE_HOSTS_FILE, "w") as f:
        for line in alive_hosts_list:
            f.write(line+"\n")
    print(f"[+] {len(alive_hosts_list)} live subdomains...")

def run() -> None:
    threads: list[Thread] = []
    
    targets: list[str] = open_subs_file(RESULTS_FILE)
    
    for url in targets:
        t: Thread = Thread(target=worker, args=(url,))
        threads.append(t)
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    log_results()
