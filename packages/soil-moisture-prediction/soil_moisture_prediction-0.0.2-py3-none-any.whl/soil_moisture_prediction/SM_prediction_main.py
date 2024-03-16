"""Command line module for soil moisture prediction."""

import argparse
import json
import logging
import os
import warnings

from RFoPrediction import RFoPrediction

# TODO catch warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument("-wd", "--workingDir", type=str)
parser.add_argument(
    "-v",
    "--verbosity",
    choices=["quiet", "verbose", "debug"],
    default="verbose",
    help="Verbosity level (quiet, verbose [default], debug)",
)
args = parser.parse_args()


def input_data():
    """Read args."""
    working_dir = args.workingDir
    with open(os.path.join(working_dir, "parameters.json"), "r") as f_handle:
        input_data = json.loads(f_handle.read())

    return RFoPrediction(input_data, working_dir)


def main():
    """Run computation."""
    # Convert string choice to corresponding numeric level
    verbosity_levels = {"quiet": 30, "verbose": 20, "debug": 10}
    selected_verbosity = verbosity_levels[args.verbosity]
    logging.basicConfig(format="%(asctime)s - %(message)s", level=selected_verbosity)

    rf_prediction = input_data()

    rf_prediction.plot_figure_selection()


if __name__ == "__main__":
    main()
