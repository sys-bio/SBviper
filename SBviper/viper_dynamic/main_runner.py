"""
Runner for time_series_matcher
"""

from util import *
import sys
import os.path
import argparse

if __name__ == "__main__":
    # original_model_path = input("The absolute path to the original model: ")
    # revised_model_path = input("The absolute path to the revised model: ")
    # original_tsc = create_tsc_from_path(original_model_path)
    # revised_tsc = create_tsc_from_path(revised_model_path)
    parser = argparse.ArgumentParser(description="Detecting changes in models")
    list_choices = ["SBML", "CSV"]
    parser.add_argument("Type", type=str, nargs="?", default="SBML",
                        help="Are you using a CSV file or a SBML file?",
                        choices=list_choices)
    args = parser.parse_args()
    path = args.Type
    if path == "SBML":
        original_model, revised_model = get_tsc_from_SBML()
    else:
        original_model, revised_model = get_tsc_from_CSV()

