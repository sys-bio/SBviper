"""
Runner for time_series_matcher
"""

from SBviper.viper_dynamic.util import *
import sys
import os.path
import argparse
from SBviper.viper_dynamic.matcher.time_series_matcher import TimeSeriesMatcher

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detecting changes in models")
    list_choices = ["SBML", "CSV", "Antimony"]
    parser.add_argument("Type", type=str, nargs="?", default="SBML",
                        help="Are you using a CSV file, a SBML model, or an "
                             "Antimony model?",
                        choices=list_choices)
    args = parser.parse_args()
    path = args.Type
    original_path = input("The absolute path to the original model: ")
    revised_path = input("The absolute path to the revised model: ")
    if path == "SBML":
        # TODO: Test this
        original_tsc, revised_tsc = get_tsc_from_SBML(original_path,
                                                          revised_path)
    elif path == "CSV":
        # TODO: Test this
        original_tsc, revised_tsc = get_tsc_from_CSV(original_path,
                                                         revised_path)
    else:  # Antimony
        original_tsc, revised_tsc = get_tsc_from_Ant(original_path,
                                                         revised_path)
    filters = input("Filters to use, separate by space: ")
    filters = filters.split()
    matcher = TimeSeriesMatcher(original_tsc, revised_tsc)
