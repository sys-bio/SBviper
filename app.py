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

sys.path.append('E:\\Research\\sys-bio\\SBviper')
sys.path.append('E:\\Research\\sys-bio\\SBviper\\SBviper')
from viper_dynamic.util import *

from viper_dynamic.matcher.time_series_matcher import TimeSeriesMatcher
from viper_dynamic.constants import str_to_function
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

import base64
from io import BytesIO

from flask import Flask, render_template, request, jsonify, send_file
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


@app.route("/run",  methods=['POST'])
def run():
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'fileDB')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    original_path_origin = request.files['original-file']
    original_path_origin.save(os.path.join(app.config['UPLOAD_FOLDER'], original_path_origin.filename))
    revised_path_origin = request.files['revised-file']
    revised_path_origin.save(os.path.join(app.config['UPLOAD_FOLDER'], revised_path_origin.filename))
    path = request.form.get("type")
    original_path = "E:\\Research\\sys-bio\\SBviper\\fileDB\\" + original_path_origin.filename
    revised_path = "E:\\Research\\sys-bio\\SBviper\\fileDB\\" + revised_path_origin.filename
    #path = 'Antimony'
    #original_path = "E:\\Research\\sys-bio\\SBviper\\tests\\experiments\\model_ant_original.txt"
    #revised_path = 'E:\\Research\\sys-bio\\SBviper\\tests\\experiments\\model_ant_original.txt'
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
    fig.savefig('images/all/' + 'all.png', format="png")

    filtered_result = []
    figureCount = 1
    for match_results in filtered_collection.match_results:
        figureCount += 1
        fig = plt.figure(figureCount)
        plt.plot(match_results.original_ts.time_points,
                           match_results.original_ts.values, color="#257F5E")
        fig.suptitle("Filtered: Original " +
                                match_results.original_ts.variable)
        fig.savefig('images/filtered/filtered_original_' + match_results.original_ts.variable + '.png', format="png")
        filtered_result.append('filtered_original_' + match_results.original_ts.variable + '.png')
        plt.close(figureCount)
        figureCount += 1
        fig = plt.figure(figureCount)
        plt.plot(match_results.revised_ts.time_points,
                           match_results.revised_ts.values, color="#8F6C05")
        fig.suptitle("Filtered: Revised " +
                                match_results.revised_ts.variable)
        fig.savefig('images/filtered/filtered_revised_' + match_results.revised_ts.variable + '.png', format="png")
        filtered_result.append('filtered_revised_' + match_results.revised_ts.variable + '.png')
        plt.close(figureCount)

    non_filtered_result = []
    for match_results in non_filtered_collection.match_results:
        figureCount += 1
        fig = plt.figure(figureCount)
        plt.plot(match_results.original_ts.time_points,
                           match_results.original_ts.values, color="#0330fc")
        fig.suptitle("Non-Filtered: Original " +
                                match_results.original_ts.variable)
        fig.savefig('images/non_filtered/non_filtered_original_' + match_results.original_ts.variable + '.png', format="png")
        non_filtered_result.append('non_filtered_original_' + match_results.original_ts.variable + '.png')
        plt.close(figureCount)
        figureCount += 1
        fig = plt.figure(figureCount)
        plt.plot(match_results.revised_ts.time_points,
                           match_results.revised_ts.values, color="#fc0303")
        fig.suptitle("Non-Filtered: Revised " +
                                match_results.revised_ts.variable)
        fig.savefig('images/non_filtered/non_filtered_revised_' + match_results.revised_ts.variable + '.png', format="png")
        non_filtered_result.append('non_filtered_revised_' + match_results.revised_ts.variable + '.png')
        plt.close(figureCount)
    combined_result = {"filtered": filtered_result, "non-filtered": non_filtered_result}
    return jsonify(combined_result)

@app.route("/images/<section1>/<section2>",  methods=['GET'])
def get_image(section1, section2):
    filename = request.path[1:]
    print(request.path)
    return send_file(filename, mimetype='image/png')
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
