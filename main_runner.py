"""
Runner for time_series_matcher
"""

from SBviper.viper_dynamic.util import *
import sys
import os.path
import argparse
from SBviper.viper_dynamic.matcher.time_series_matcher import TimeSeriesMatcher
from SBviper.viper_dynamic.constants import str_to_function
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# matplotlib.use('TkAgg')
matplotlib.use('WebAgg')

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
    # add filters to matcher
    for filter_str in filters:
        if filter_str in str_to_function:
            matcher.add_filter(str_to_function[filter_str])
        else:
            print(filter_str + " does not exist!")
    # run filters
    filtered_collection, non_filtered_collection = matcher.run()
    # show result
    fig, axs = plt.subplots(ncols=2, nrows=len(filtered_collection) +
                                           len(non_filtered_collection))
    index = 0
    for match_results in filtered_collection.match_results:
        axs[index, 0].plot(match_results.original_ts.time_points,
                           match_results.original_ts.values, color="#257F5E")
        axs[index, 0].set_title("Filtered: Original " +
                                match_results.original_ts.variable)
        axs[index, 1].plot(match_results.revised_ts.time_points,
                           match_results.revised_ts.values, color="#8F6C05")
        axs[index, 1].set_title("Filtered: Revised " +
                                match_results.revised_ts.variable)
        index += 1
    for match_results in non_filtered_collection.match_results:
        print("A")
        axs[index, 0].plot(match_results.original_ts.time_points,
                           match_results.original_ts.values, color="#0330fc")
        axs[index, 0].set_title("Non-Filtered: Original " +
                                match_results.original_ts.variable)
        axs[index, 1].plot(match_results.revised_ts.time_points,
                           match_results.revised_ts.values, color="#fc0303")
        axs[index, 1].set_title("Non-Filtered: Revised " +
                                match_results.revised_ts.variable)
        index += 1
    fig.tight_layout()
    plt.show()
