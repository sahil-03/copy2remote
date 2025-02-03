import argparse 
import json
import os
import subprocess 
from pathlib import Path

CONFIGS_DIR_PATH = Path(__file__).parent / "configs"

def _run_command(command: str): 
    try: 
        _ = subprocess.run(
            command, 
            shell=True, 
            text=True, 
            capture_output=False, 
            check=False,
        )
    except Exception as e: 
        print(f"Subprocess failed with error: {e}")

def copy_to_remote(config_num: int, custom_hostname: str = None): 
    config_file = f"{CONFIGS_DIR_PATH}/config{config_num}.json"
    with open(config_file, "r") as f:
        data = json.load(f)

    if data["has_gh"]: 
        print("Pulling latest from GitHbub")
        original_dir = os.getcwd() 
        try: 
            os.chdir(data["local_path"])
            _run_command("git pull")
        finally: 
            os.chdir(original_dir)
    
    key_file_str = "-i {}".format(data["key_filename"])
    command = "scp -r {} {} {}@{}:~/".format(
        key_file_str if data["key_filename"] else "", 
        data["local_path"], 
        data["username"], 
        custom_hostname if custom_hostname is not None else data["hostname"]
    )
    _run_command(command)

def create_new_config(args_dict: dict): 
    new_config_num = len(os.listdir(CONFIGS_DIR_PATH)) + 1
    new_config_file = f"{CONFIGS_DIR_PATH}/config{new_config_num}.json"
    with open(new_config_file, "w") as f:
        json.dump(args_dict, f, indent=4) 
    
    print(f"Created a new config #{new_config_num} with the following contents:\n\n{args_dict}")

def list_all_configs(verbose: bool = False): 
    for file in os.listdir(CONFIGS_DIR_PATH): 
        print(f"{file}")

        if verbose: 
            with open(f"{CONFIGS_DIR_PATH}/{file}", "r") as f:
                data = json.load(f) 
            for k, v in data.items(): 
                print(f"\t{k}: {v}")
        print()
    
    print("Completed printing all existing configs.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser() 
    subparsers = parser.add_subparsers(dest="command")

    # run a config
    parser.add_argument('-r', '--run', type=int, help='Run config number')
    parser.add_argument('--host', default=None, help='Run with a custom hostname')
    
    # "new" command
    new_parser = subparsers.add_parser("new", aliases=["n"])
    new_parser.add_argument("local_path", help="Local path")
    new_parser.add_argument("username", help="Username")
    new_parser.add_argument("hostname", help="Hostname")
    new_parser.add_argument("key_filename", help="Key filename, optional", default=None)
    new_parser.add_argument("has_gh", help="Associated github repo, optional", default=False)

    # "list" command
    list_parser = subparsers.add_parser("list", aliases=["ls"])
    list_parser.add_argument("-v", "--verbose", action="store_true", help="List all files and their contents")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.run is not None: 
        copy_to_remote(args.run, args.host)
    elif args.command in ["new", "n"]:
        create_new_config(args.__dict__)
    elif args.command in ["list", "ls"]: 
        list_all_configs(args.verbose)
