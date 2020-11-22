"""
Runner for time_series_matcher
"""

from SBviper.viper_dynamic.util import *
import sys
import os.path
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detecting changes in models")
    list_choices = ["SBML", "CSV"]
    parser.add_argument("Type", type=str, nargs="?", default="SBML",
                        help="Are you using a CSV file or a SBML file?",
                        choices=list_choices)
    args = parser.parse_args()
    path = args.Type
    original_path = input("The absolute path to the original model: ")
    revised_path = input("The absolute path to the revised model: ")
    if path == "SBML":
        original_model, revised_model = get_tsc_from_SBML(original_path,
                                                          revised_path)
    else:
        # TODO: Test this
        original_model, revised_model = get_tsc_from_CSV(original_path,
                                                         revised_path)

