# __init__.py

import importlib
import os

def run_script(script_name):
    try:
        module = importlib.import_module(script_name)
        print(f"Executed {script_name} successfully.")
    except Exception as e:
        print(f"Error executing {script_name}: {str(e)}")

def main():
    scripts = [
        "watch_consoles",
        "shared_links_management",
        "cavaillon_shared_links",
        "leogane_shared_links",
        "terre_neuve_shared_links",
        "ferrier_shared_links",
        "pignon_shared_links",
        "hanwash_overall_shared_links"
    ]

    print("Executing mWater dashboard scripts...")
    
    for script in scripts:
        run_script(script)

    print("\nAll scripts executed. Check the ./ui/components/ directory for the generated Excel files.")

if __name__ == "__main__":
    main()
