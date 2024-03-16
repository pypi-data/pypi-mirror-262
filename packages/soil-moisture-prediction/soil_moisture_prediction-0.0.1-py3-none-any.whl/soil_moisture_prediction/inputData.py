"""Load and process input data."""

import json
import logging
import math
import os
from builtins import len

import numpy as np
from scipy import ndimage
from scipy.interpolate import griddata
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


class SoilMoistureData:
    """Class containing soil moisture measurements."""

    x_measurement = {}
    y_measurement = {}
    soil_moisture = {}
    start_times = []
    number_measurements = {}
    soil_moisture_dev_low = {}
    soil_moisture_dev_high = {}

    def __init__(self, soil_moisture_file, geom, uncertainty):
        """Open soil moisture file and save data to np arrays."""
        logger.info("Loading soil moisture data...")

        self.open_soil_moisture_file(soil_moisture_file, geom, uncertainty)

    def open_soil_moisture_file(self, soil_moisture_file, geom, uncertainty):
        """Open soil moisture file and save data to np arrays."""
        with open(soil_moisture_file, "r") as sm:
            lines = sm.readlines()
            for row in lines[1:]:
                row_values = row.split(",")
                start_time = row_values[2]
                if start_time not in self.number_measurements:
                    self.initiate_sm_arrays(start_time, uncertainty)
                self.update_sm_arrays(row_values, start_time, geom, uncertainty)

            self.start_times = list(self.number_measurements.keys())

            for start_time in self.start_times:
                self.x_measurement[start_time] = np.array(
                    self.x_measurement[start_time]
                )
                self.y_measurement[start_time] = np.array(
                    self.y_measurement[start_time]
                )
                self.soil_moisture[start_time] = np.array(
                    self.soil_moisture[start_time]
                )
                if uncertainty:
                    self.soil_moisture_dev_low[start_time] = np.array(
                        self.soil_moisture_dev_low[start_time]
                    )
                    self.soil_moisture_dev_high[start_time] = np.array(
                        self.soil_moisture_dev_high[start_time]
                    )
                # TODO sort by measurement time

    def initiate_sm_arrays(self, start_time, uncertainty):
        """Initiate lists to store sm data for the given start_time."""
        self.number_measurements[start_time] = 0
        self.x_measurement[start_time] = []
        self.y_measurement[start_time] = []
        self.soil_moisture[start_time] = []
        if uncertainty:
            self.soil_moisture_dev_low[start_time] = []
            self.soil_moisture_dev_high[start_time] = []

    def update_sm_arrays(self, sm_file_values, start_time, geom, uncertainty):
        """Update lists to store sm data for the given start_time.

        If the given point is outside the area, it is discarded.
        """
        x = float(sm_file_values[0])
        y = float(sm_file_values[1])
        nearest_node = geom.find_nearest_node(x, y)
        if nearest_node[0, 0] < geom.dim_x and nearest_node[0, 1] < geom.dim_y:
            self.x_measurement[start_time].append(x)
            self.y_measurement[start_time].append(y)
            self.soil_moisture[start_time].append(float(sm_file_values[3]))
            if uncertainty:
                self.soil_moisture_dev_low[start_time].append(
                    abs(float(sm_file_values[4]))
                )
                self.soil_moisture_dev_high[start_time].append(float(sm_file_values[5]))
            self.number_measurements[start_time] += 1


class InputData:
    """Class containing all input data, predictors and soil moisture measurements."""

    number_predictors = 0
    predictors = {}
    training_coordinates = {}
    training_pred = {}
    _correlation_matrix = np.empty((number_predictors, number_predictors))

    def __init__(
        self,
        predictor_files,
        soil_moisture_file,
        geom,
        uncertainty,
        apply_pca=False,
        has_mask=False,
    ):
        """Initialize input data."""
        self.pred_files = predictor_files
        self.uncertainty = uncertainty
        # TODO maybe delete?
        self.has_mask = has_mask
        self.apply_pca = apply_pca
        self.soil_moisture_data = SoilMoistureData(
            soil_moisture_file, geom, uncertainty
        )

    def prepare_predictors(self, geom, compute_slope_aspect=True, use_prediction=False):
        """Interpolate predictors to project grid.

        If applicable, compute slope and aspect from elevation
        Compute number of predictors
        If applicable, compute predictor correlation matrix
        Extract predictor values at the training locations
        """
        self.fit_predictors_to_grid(geom)

        self.uniformize_nan_across_predictors(geom)

        if compute_slope_aspect:
            self.compute_slope_aspect()
        self.number_predictors = len(self.predictors)

        if use_prediction:
            self.number_predictors += 1
            self.predictors["past_prediction"] = (
                np.zeros((geom.dim_x, geom.dim_y)),
                "g/g",
            )

        self.prepare_training_predictors(geom)

    def fit_predictors_to_grid(self, geom):
        """Open a predictor file and interpolate.

        Interpolate it to a 2D array corresponding to the project geometry
        Returns: self.predictors dictionary with pred_name as key, interpolated array
        and unit as values
        """
        logger.info("Loading predictors and interpolating them to project grid.")
        for pred_name, pred_values in self.pred_files.items():
            x = []
            y = []
            predictor = []
            with open(pred_values[0], "r") as ft:
                for row in ft:
                    line = row.split(",")
                    buffer_width = 10
                    if self.is_pixel_within_area(line, buffer_width, geom):
                        x.append(float(line[0]))
                        y.append(float(line[1]))
                        predictor.append(float(line[2]))
            predictor_on_nodes = griddata(
                (x, y), predictor, (geom.grid_x, geom.grid_y), method="linear"
            )
            self.predictors[pred_name] = (predictor_on_nodes, pred_values[1])

    def is_pixel_within_area(self, line, buffer_width, geom):
        """Check if the given predictor pixel is within the study area."""
        pixel_inside = False
        if (
            geom.xi - buffer_width * geom.resolution
            <= float(line[0])
            <= geom.xf + buffer_width * geom.resolution
            and geom.yi - buffer_width * geom.resolution
            <= float(line[1])
            <= geom.yf + buffer_width * geom.resolution
            and float(line[2]) > 0
        ):
            pixel_inside = True
        return pixel_inside

    # Check how to deal with None
    def uniformize_nan_across_predictors(self, geom):
        """If NAN are found in a predictor set pixel to NAN for all other predictors."""
        nan_indexes = np.full((geom.dim_x, geom.dim_y), False)
        for pred_values in self.predictors.values():
            nan_indexes[np.isnan(pred_values[0])] = True
        for pred_name in self.predictors.keys():
            self.predictors[pred_name][0][nan_indexes] = np.nan

    def compute_slope_aspect(self, compute_aspect=True):
        """Compute slope and aspect map from an elevation map."""
        if "elevation" not in self.predictors:
            logging.warning('Can not compute slope. No "elevation" data set found')
            return
        logger.info("Computing slope and aspects from elevation dataset...")
        elev_dx, elev_dy = np.gradient(self.predictors["elevation"][0])
        self.predictors["slope"] = (
            np.sqrt(elev_dx * elev_dx + elev_dy * elev_dy),
            "m/m",
        )
        if compute_aspect:
            aspect = np.arctan2(-elev_dx, elev_dy)
            self.predictors["aspect_we"] = (90 - 90 * np.sin(aspect), "degree")
            self.predictors["aspect_ns"] = (90 - 90 * np.cos(aspect), "degree")

    def compute_correlation_matrix(self):
        """Compute the correlation matrix between all predictors (2 by 2)."""
        # TODO : remove half computations since symmetric matrix
        if self._correlation_matrix.size != 0:
            return self._correlation_matrix
        logger.info("Computing correlation between predictors...")
        self._correlation_matrix = np.zeros(
            (self.number_predictors, self.number_predictors)
        )
        i = 0
        for pred1 in self.predictors.values():
            j = 0
            for pred2 in self.predictors.values():
                self._correlation_matrix[i, j] = self._compute_pred_correlation(
                    pred1[0], pred2[0]
                )
                j += 1
            i += 1
        return self._correlation_matrix

    def _compute_pred_correlation(self, arr1, arr2):
        """Compute the 2-D correlation coefficient (scalar) between two 2d arrays.

        arr1, arr2:  numpy 2D arrays
        """
        arr1_nonan = np.ma.array(arr1, mask=np.isnan(arr1))
        arr2_nonan = np.ma.array(arr2, mask=np.isnan(arr2))

        arr1_mean = np.sum(arr1_nonan) / np.size(arr1_nonan)
        arr2_mean = np.sum(arr2_nonan) / np.size(arr2_nonan)

        arr1_norm = arr1_nonan - arr1_mean
        arr2_norm = arr2_nonan - arr2_mean

        correlation_coeff = (arr1_norm * arr2_norm).sum() / math.sqrt(
            (arr1_norm * arr1_norm).sum() * (arr2_norm * arr2_norm).sum()
        )
        return correlation_coeff

    def prepare_training_predictors(self, geom):
        """Extract predictor values at training locations and save them in a array."""
        for start_time in self.soil_moisture_data.start_times:
            self.training_coordinates[start_time] = np.zeros(
                ((self.soil_moisture_data.number_measurements[start_time]), 2),
                dtype=int,
            )
            self.training_coordinates[start_time] = geom.find_nearest_node(
                self.soil_moisture_data.x_measurement[start_time],
                self.soil_moisture_data.y_measurement[start_time],
            )
            self.set_training_predictors(start_time)

    def set_training_predictors(self, start_time):
        """Set the training predictors for the given start_time."""
        self.training_pred[start_time] = np.empty(
            (
                self.soil_moisture_data.number_measurements[start_time],
                self.number_predictors,
            )
        )
        for coord_index, coord in enumerate(self.training_coordinates[start_time]):
            self.training_pred[start_time][coord_index] = [
                pred[0][coord[0], coord[1]] for pred in self.predictors.values()
            ]

    # TODO review the whole mask stuff
    def apply_mask(self, geom, mask):
        """Open and interpolate the mask file.

        Set all predictors to NaN following the mask given in argument
        Remove training points where predictors are NaN
        """
        with open(mask, "r") as ft:
            lines = ft.readlines()
            mask_xyz = np.zeros((len(lines), 3))
            for i, j in enumerate(lines):
                line = j.split()
                if line[2] == "urban" or line[2] == "water":
                    mask_xyz[i, :] = [float(line[0]), float(line[1]), np.nan]
                else:
                    mask_xyz[i, :] = [float(line[0]), float(line[1]), 1]
        mask_grid = griddata(
            (mask_xyz[:, 0], mask_xyz[:, 1]),
            mask_xyz[:, 2],
            (geom.grid_x, geom.grid_y),
            method="linear",
        )

        self.has_mask = True
        self.mask = mask_grid

        for k, p in self.predictors.items():
            self.predictors[k] = (p[0] * self.mask, p[1])

        idx_no_nan = []
        for i, pts in enumerate(self.pts_train):
            if np.isnan(mask[pts[0], pts[1]]) is False:
                idx_no_nan.append(i)

        self.x_measurement = self.x_measurement[idx_no_nan]
        self.y_measurement = self.y_measurement[idx_no_nan]
        self.pts_train = self.pts_train[idx_no_nan]
        self.feat_train = self.feat_train[idx_no_nan]
        self.n_pts = len(idx_no_nan)

        sm_no_nan = np.empty((self.number_time_intervals, self.n_pts))
        for time_step in range(self.number_time_intervals):
            sm_no_nan[time_step] = self.soil_moisture[time_step][idx_no_nan]
        self.soil_moisture = sm_no_nan

    # TODO review whole pca stuff
    def use_pca(self, n_components):
        """Apply a principal component analysis to reduce the number of features.

        n_components: Number of components to keep
        """
        pca = PCA(n_components=n_components)
        pca_feat = pca.fit_transform(self.feat_train)
        self.feat_train = pca_feat
        self.number_predictors = n_components
        self.pca = pca
        logger.info(f"PCA explained variance ration: {pca.explained_variance_ratio_}")

    def check_no_nan_in_training(self, day):
        """Check at each training locations if a predictor is NAN.

        In this case, the measurement is discarded.
        """
        for coord in self.training_coordinates[day]:
            for pred in self.predictors.values():
                if np.isnan(pred[0][coord[0], coord[1]]):
                    raise ValueError("NAN in measurement!")

    def soil_moisture_filering(self, start_time):
        """Apply median filter to the measurements."""
        x = self.soil_moisture_data.x_measurement[start_time]
        y = self.soil_moisture_data.y_measurement[start_time]
        branches = self.separate_branches(
            x / 1000, y / 1000, self.soil_moisture_data.soil_moisture[start_time]
        )
        filtered_branches = [
            ndimage.median_filter(branch[:, 2], size=5) for branch in branches
        ]
        self.soil_moisture_data.soil_moisture[start_time] = np.concatenate(
            filtered_branches
        )

    def separate_branches(self, x, y, z, threshold_distance=1):
        """Identify branch transitions based on distance between consecutive points."""
        # Threshold by time when time data input is added?
        distances = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2)
        branch_transitions = np.where(distances > threshold_distance)[0] + 1
        branches = np.split(np.column_stack([x, y, z]), branch_transitions)
        return branches

    # TODO Change variable names days to time interval
    def average_measurements_over_days(self, current_day, n_days_average):
        """Average soil moisture measurements over the previous days."""
        if len(self.self.soil_moisture_data.start_times) < n_days_average:
            logging.warning(
                "Will not apply averge over time intervals. Not enough intervals!"
            )
            return
        self.sm_train = self.soil_moisture_data.soil_moisture[current_day, :]
        for day in range(1, n_days_average):
            self.sm_train += self.soil_moisture_data.soil_moisture[current_day - day, :]
        self.sm_train /= n_days_average

    def check_rainfall_occurences(self, n_timesteps_reset, timestep):
        """Check if rainfall occurred in the previous days."""
        had_rainfall = False
        for time_step in range(n_timesteps_reset):
            time_to_check = self.soil_moisture_data.start_times[timestep - time_step]
            timestep_rainfall = self.get_timestep_rainfall(time_to_check)
            if timestep_rainfall > 0:
                had_rainfall = True
                break
        return had_rainfall

    def get_timestep_rainfall(self, time_to_check):
        """Get the rainfall value for the given time step."""
        # TODO decide if removing test or coding rainfall reading correctly
        working_dir = r"C:\Users\dega\Documents\UQ\UQ_script\Ruebeland"
        file_path = os.path.join(working_dir, "rainfall_values.json")
        with open(file_path, "r") as json_file:
            rainfall_values = json.load(json_file)
        timestep_rainfall = rainfall_values[time_to_check]
        return timestep_rainfall
