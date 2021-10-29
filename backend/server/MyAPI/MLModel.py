from scipy.optimize import lsq_linear
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import numpy as np
import numbers
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold
from sklearn.base import clone
from sklearn.model_selection import cross_val_score
from . models import ResultsNNLS, ResultsOLS


NNLS = 0
OLS = 1


def get_mode_name(mode):
    '''Return name of the current mode.'''
    return ('OLS' if i == OLS else 'NNLS')


def get_file_label(mode):
    '''Return filesystem-friendly name of the regressand field.'''
    return ('Energy' if 'Energy' in mode else 'Cycles')


def display_scores(scores):
    print("Scores: ", scores)
    print("Mean: ", scores.mean())
    print("Standard deviation: ", scores.std())


# df = pd.read_csv("stats_and_modeling/COMBINED/48/1/0/data-HW-and-TL.csv")
# param_list = ['Executed insns (no MULS)', 'MULS insns', 'Taken branches', 'RAM data reads', 'RAM writes', 'Flash data reads', 'Flash insn reads', 'BL insns', 'PUSH/POP PC/LR']
# target_column = 'HW Cycles (IT adjusted)'
# adjust = 1.0
# round = 5
# threshold = 5.0 / 100


def get_data(df, param_list, target_column, adjust, round, threshold):

    param_list = eval(param_list)
    y = df.loc[:, target_column].values
    # Adjust the regressand.
    if adjust is not None:
        y = y * adjust
    fixed = "{}"
    param_value_dict = eval(fixed)
    fixed_params = param_value_dict.keys()
    unconstrained_params = []

    if param_value_dict:
        for param in param_list:
            if param in fixed_params and isinstance(param_value_dict[param], numbers.Number):
                # Subtract the contribution of the param from the Y vector
                print('')
                print("Ratio of residual/original")
                print(
                    (y - (df.loc[:, param].values * param_value_dict[param])) / y)
                print('')
                y = y - (df.loc[:, param].values * param_value_dict[param])
            else:
                unconstrained_params.append(param)
        # Reset param list to the free-running parameters only.
        param_list = unconstrained_params
    else:
        pass

    x = df.loc[:, param_list].values
    regressor = LinearRegression(fit_intercept=False)
    rkf = RepeatedKFold(n_splits=10, n_repeats=1, random_state=None)
    scrs = []
    count = 0
    for train_index, test_index in rkf.split(x):
        clone_regressor = clone(regressor)
        #print("Train:", train_index, "\nValidation:", test_index)
        X_train, X_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clone_regressor.fit(X_train, y_train)
        y_pred = clone_regressor.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        scrs.append(rmse)
        count = count + 1

    scrs_array = np.asarray(scrs)
    display_scores(scrs_array)

    # Evaluate score by cross validation
    regressor2 = LinearRegression(fit_intercept=False)
    scores = cross_val_score(
        regressor2, x, y, scoring="neg_mean_squared_error", cv=10)
    try:
        rmse_scores = np.sqrt(-scores)
    except:
        print("### np.sqrt(-scores) failed, scores = " + str(scores))
    display_scores(rmse_scores)

    coefs = [None] * 2
    predicted = [None] * 2
    outliers = [None] * 2

    # Final model using all data
    regressor3 = LinearRegression(fit_intercept=False)
    regressor3.fit(x, y)
    pred = regressor3.predict(x)
    # print(param_list)
    coefs[OLS] = regressor3.coef_
    predicted[OLS] = pred

    #print("Coefficients constrained to non-negative values, least-squares method")

    lb = 0
    ub = np.Inf
    res = lsq_linear(x, y, bounds=(lb, ub))

    # Round the coefficients if requested to.
    # print(param_list)
    if round is not None:
        res.x = np.round(res.x, round)

    # with np.printoptions(linewidth=200):
    #    print(res.x)

    coefs[NNLS] = res.x
    predicted[NNLS] = np.dot(x, res.x)

    # mean_abs_percentage_error = [None] * 2
    # percentage_error_vect = [None] * 2
    # mean_percentage_error = [None] * 2
    # median_percentage_error = [None] * 2
    # mean_squared_RE = [None] * 2
    # rmsre = [None] * 2
    # stddev_abs_percentage_error = [None] * 2
    # stddev_relative_error = [None] * 2
    # mse = [None] * 2
    # rmse = [None] * 2

    resultsNNLS = ResultsNNLS()
    resultsOLS = ResultsOLS()

    for i in [NNLS, OLS]:
        if i == NNLS:
            resultsNNLS.outliers = str([(bench, predicted, actual, 100 * (predicted - actual) / actual) if abs(predicted - actual) /
                                        actual > threshold else None for (bench, predicted, actual) in zip(df.loc[:, 'Bench'], predicted[i], y)])

            # Determine and print mean(abs(relative error)).
            mean_abs_percentage_error = mean_absolute_error(
                y / y, predicted[i] / y) * 100.0
            resultsNNLS.mean_abs_percentage_error = mean_abs_percentage_error
            # print("MAPE_%s = %.5f%%" %
            #       (get_mode_name(i), mean_abs_percentage_error[i] * 100.0))

            # Determine and print mean(percentage error).
            percentage_error_vect = predicted[i] / y - y / y
            mean_percentage_error = (
                percentage_error_vect).mean() * 100.0
            resultsNNLS.mean_percentage_error = mean_percentage_error
            resultsNNLS.percentage_error_vect = str(percentage_error_vect)
            # print("MEAN(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), mean_percentage_error[i] * 100.0))

            # Determine and print the median error.
            resultsNNLS.median_percentage_error = np.median(
                percentage_error_vect) * 100.0
            # print("MEDIAN(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), median_percentage_error[i] * 100.0))

            # Determine and print root of mean square relative error.
            mean_squared_RE = mean_squared_error(y / y, predicted[i] / y)
            resultsNNLS.rmsre = np.sqrt(mean_squared_RE) * 100.0
            # print("rootMSRE_%s = %.5f%%" % (get_mode_name(i), rmsre[i] * 100.0))

            resultsNNLS.stddev_abs_percentage_error = np.sqrt(mean_squared_error(np.full(
                y.shape, mean_abs_percentage_error), predicted[i] / y - np.full(y.shape, 1.0))) * 100.0
            # print("STDDEV(MAPE_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_abs_percentage_error[i] * 100.0))

            resultsNNLS.stddev_relative_error = np.sqrt(mean_squared_error(np.full(
                y.shape, mean_percentage_error), predicted[i] / y - np.full(y.shape, 1.0))) * 100.0
            # print("STDDEV(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_relative_error[i] * 100.0))

            mse = mean_squared_error(y, predicted[i])
            rmse = np.sqrt(mse)
            r2 = r2_score(y, predicted[i])
            resultsNNLS.rmse = str(rmse)
            resultsNNLS.r2_score = str(r2)
            resultsNNLS.save()
            # print(("RMSE Score %s:" % get_mode_name(i)) + str(rmse))
            # print(("R2 Score %s:" % get_mode_name(i)) + str(r2_score(y, predicted[i])))

            # print("List of %d/%d outliers using %s at threshold %.2f%% (predicted, actual, error in %%):" %
            #       (len(list(filter(None, outliers[i]))), len(outliers[i]), get_mode_name(i), threshold * 100.0))
            # print("=================================================")
            # [print("%s: %.9f, %.9f, %5.2f%%" % elt)
            #  if elt else None for elt in outliers[i]]
        else:
            resultsOLS.outliers = str([(bench, predicted, actual, 100 * (predicted - actual) / actual) if abs(predicted - actual) /
                                       actual > threshold else None for (bench, predicted, actual) in zip(df.loc[:, 'Bench'], predicted[i], y)])

            # Determine and print mean(abs(relative error)).
            mean_abs_percentage_error = mean_absolute_error(
                y / y, predicted[i] / y) * 100.0
            resultsOLS.mean_abs_percentage_error = mean_abs_percentage_error
            # print("MAPE_%s = %.5f%%" %
            #       (get_mode_name(i), mean_abs_percentage_error[i] * 100.0))

            # Determine and print mean(percentage error).
            percentage_error_vect = predicted[i] / y - y / y
            mean_percentage_error = (
                percentage_error_vect).mean() * 100.0
            resultsOLS.mean_percentage_error = mean_percentage_error
            resultsOLS.percentage_error_vect = str(percentage_error_vect)
            # print("MEAN(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), mean_percentage_error[i] * 100.0))

            # Determine and print the median error.
            resultsOLS.median_percentage_error = np.median(
                percentage_error_vect) * 100.0
            # print("MEDIAN(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), median_percentage_error[i] * 100.0))

            # Determine and print root of mean square relative error.
            mean_squared_RE = mean_squared_error(y / y, predicted[i] / y)
            resultsOLS.rmsre = np.sqrt(mean_squared_RE) * 100.0
            # print("rootMSRE_%s = %.5f%%" % (get_mode_name(i), rmsre[i] * 100.0))

            resultsOLS.stddev_abs_percentage_error = np.sqrt(mean_squared_error(np.full(
                y.shape, mean_abs_percentage_error), predicted[i] / y - np.full(y.shape, 1.0))) * 100.0
            # print("STDDEV(MAPE_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_abs_percentage_error[i] * 100.0))

            resultsOLS.stddev_relative_error = np.sqrt(mean_squared_error(np.full(
                y.shape, mean_percentage_error), predicted[i] / y - np.full(y.shape, 1.0))) * 100.0
            # print("STDDEV(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_relative_error[i] * 100.0))

            mse = mean_squared_error(y, predicted[i])
            rmse = np.sqrt(mse)
            r2 = r2_score(y, predicted[i])
            resultsOLS.rmse = str(rmse)
            resultsOLS.r2_score = str(r2)
            resultsOLS.save()
            # print(("RMSE Score %s:" % get_mode_name(i)) + str(rmse))
            # print(("R2 Score %s:" % get_mode_name(i)) + str(r2_score(y, predicted[i])))

            # print("List of %d/%d outliers using %s at threshold %.2f%% (predicted, actual, error in %%):" %
            #       (len(list(filter(None, outliers[i]))), len(outliers[i]), get_mode_name(i), threshold * 100.0))
            # print("=================================================")
            # [print("%s: %.9f, %.9f, %5.2f%%" % elt)
            #  if elt else None for elt in outliers[i]]
