#!/usr/bin/env python3

import sys
import os

# Check Python version
if sys.version_info < (3, 6):
    print("Python 3.6 or later is required to run this script.")
    sys.exit(1)

# Add the path to the directory containing simple_term_menu.py to the system path
simple_term_menu_path = os.path.join(os.path.dirname(__file__), "..", "simple_term_menu")
sys.path.insert(0, simple_term_menu_path)

import time
import argparse
from simple_term_menu import TerminalMenu


def get_directories(start_dir, source):
    # Get all visible directories in the specified path that contain a
    # Makefile under the specified source directory or the default "src" directory
    directories = []
    for d in os.listdir(start_dir):
        if os.path.isdir(os.path.join(start_dir, d)) and not d.startswith('.'):
            makefile_path = os.path.join(start_dir, d, source, "Makefile")
            if os.path.isfile(makefile_path):
                directories.append(d)
    return directories


def prompt_selection(directories):
    menu = TerminalMenu(directories, title="Select available directories to clean and build:", status_bar="Use up/down arrow keys in your keyboard to scroll.",  multi_select=True, show_multi_select_hint=True, menu_cursor=("=>"))
    selected_indices = menu.show()
    return [directories[i] for i in selected_indices]


def execute_commands(selected_dirs, start_dir, source, suppress_confirmation, sleep_time):
    # Confirmation prompt
    if not suppress_confirmation:
        print("Selected directories to clean and build:")
        for dir_name in selected_dirs:
            src_path = os.path.join(start_dir, dir_name, source)
            print(f"[*] {src_path}")
        print("")

        confirmation = input("Are you sure you want to clean and build the selected directories? (yes/no): ").lower()
        if confirmation != 'yes':
            print("Aborting operation. Thanks!")
            exit(0)

    # Display message with command to execute
    print("Executing command in {} seconds:".format(sleep_time))
    for dir_name in selected_dirs:
        src_path = os.path.join(start_dir, dir_name, source)
        command = f"make clean all -C '{src_path}'"
        print(f"  {command}")
        # Wait for specified seconds
        time.sleep(sleep_time)
        os.system(command)
    

def main():
    parser = argparse.ArgumentParser(description="Clean and build selected directories.")
    parser.add_argument("-d", "--dir", help="Absolute or relative path to start directory scanning. Default is current directory.", default=os.getcwd())
    parser.add_argument("-s", "--source", help="The source directory inside the selected directory. Default is src", default="src")
    parser.add_argument("-y", "--yes", action="store_true", help="Suppress confirmation. Default is do not suppress.")
    parser.add_argument("-w", "--wait", type=int, default=10, help="Time to wait in seconds before executing the command. Default is 10 seconds.")

    args = parser.parse_args()

    # Get the directories
    start_dir = os.path.abspath(args.dir)
    directories = get_directories(start_dir, args.source)

    # Check if there are visible directories
    if not directories:
        print(f"No sub-directory found with source directory '{args.source}' containing a Makefile under '{start_dir}'. Aborting!!!")
        exit(1)

    selected_dirs = prompt_selection(directories)
    execute_commands(selected_dirs, start_dir, args.source, args.yes, args.wait)


if __name__ == "__main__":
    main()
