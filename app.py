"""
=============================================
Embedding in a web application server (Flask)
=============================================

When using Matplotlib in a web server it is strongly recommended to not use
pyplot (pyplot maintains references to the opened figures to make
`~.matplotlib.pyplot.show` work, but this will cause memory leaks unless the
figures are properly closed).

Since Matplotlib 3.1, one can directly create figures using the `.Figure`
constructor and save them to in-memory buffers.  In older versions, it was
necessary to explicitly instantiate an Agg canvas (see e.g.
:doc:`/gallery/user_interfaces/canvasagg`).

The following example uses Flask_, but other frameworks work similarly:

.. _Flask: https://flask.palletsprojects.com

"""
import sys
import os.path
import argparse

sys.path.append('C:\\Frank\\research\\SBviper')
sys.path.append('C:\\Frank\\research\\SBviper\\SBviper')
print(sys.path)
from viper_dynamic.util import *

from viper_dynamic.matcher.time_series_matcher import TimeSeriesMatcher
from viper_dynamic.constants import str_to_function
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import base64
from io import BytesIO

from flask import Flask, render_template, request
from matplotlib.figure import Figure

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/pic")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


@app.route("/run")
def run():
    path = request.args.get('type')
    print(path)

    original_path = "C:\\Frank\\research\SBviper\\tests\\experiments\\model_ant_original.txt"
    revised_path = 'C:\\Frank\\research\SBviper\\tests\\experiments\\model_ant_original.txt'
    if path == "SBML":
        # TODO: Test this
        original_tsc, revised_tsc = get_tsc_from_SBML(original_path,
                                                      revised_path)
    elif path == "CSV":
        # TODO: Test this
        original_tsc, revised_tsc = get_tsc_from_CSV(original_path,
                                                     revised_path)
    else:  # Antimony
        print(original_path)
        print(revised_path)
        original_tsc, revised_tsc = get_tsc_from_Ant(original_path,
                                                     revised_path)
    filters = "frechet_distance"
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
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

#############################################################################
#
# Since the above code is a Flask application, it should be run using the
# `flask command-line tool <https://flask.palletsprojects.com/en/master/cli/>`_
# Assuming that the working directory contains this script:
#
# Unix-like systems
#
# .. code-block:: console
#
#  FLASK_APP=web_application_server_sgskip flask run
#
# Windows
#
# .. code-block:: console
#
#  set FLASK_APP=web_application_server_sgskip
#  flask run
#
#
# Clickable images for HTML
# -------------------------
#
# Andrew Dalke of `Dalke Scientific <http://www.dalkescientific.com>`_
# has written a nice `article
# <http://www.dalkescientific.com/writings/diary/archive/2005/04/24/interactive_html.html>`_
# on how to make html click maps with Matplotlib agg PNGs.  We would
# also like to add this functionality to SVG.  If you are interested in
# contributing to these efforts that would be great.
