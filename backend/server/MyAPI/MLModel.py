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
from . models import Parameters, Results
import ast
from django.utils import timezone


NNLS = 0
OLS = 1

results = Results()

def get_mode_name(mode):
    '''Return name of the current mode.'''
    return ('OLS' if i == OLS else 'NNLS')


def get_file_label(mode):
    '''Return filesystem-friendly name of the regressand field.'''
    return ('Energy' if 'Energy' in mode else 'Cycles')


def display_scores(scores, round):
    # print("Scores: ", scores)
    # print("Mean: ", scores.mean())
    # print("Standard deviation: ", scores.std())
    return str([np.round(num, round) for num in list(scores)]), np.round(scores.mean(), round), np.round(scores.std(), round)

# df = pd.read_csv("stats_and_modeling/COMBINED/48/1/0/data-HW-and-TL.csv")
# param_list = ['Executed insns (no MULS)', 'MULS insns', 'Taken branches', 'RAM data reads', 'RAM writes', 'Flash data reads', 'Flash insn reads', 'BL insns', 'PUSH/POP PC/LR']
# target_column = 'HW Cycles (IT adjusted)'
# adjust = 1.0
# round = 5
# threshold = 5.0 / 100


def get_data(df, param_list, target_column, adjust, round, fixed, threshold):

    param_list = eval(param_list)
    y = df.loc[:, target_column].values
    results.y = str(list(y))
    # Adjust the regressand.
    if adjust is not None:
        y = y * adjust
        results.y = str(list(y))
    else:
        pass
    if fixed is not None:
        fixed_dict = fixed
        param_value_dict = ast.literal_eval(fixed_dict)
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
    results.rkf_scores, results.rkf_mean, results.rkf_stddev = display_scores(
        scrs_array, round)

    # Evaluate score by cross validation
    regressor2 = LinearRegression(fit_intercept=False)
    scores = cross_val_score(
        regressor2, x, y, scoring="neg_mean_squared_error", cv=10)
    try:
        rmse_scores = np.sqrt(-scores)
    except:
        print("### np.sqrt(-scores) failed, scores = " + str(scores))
    results.cv_scores, results.cv_mean, results.cv_stddev = display_scores(rmse_scores, round)

    coefs = [None] * 2
    predicted = [None] * 2
    outliers = [None] * 2

    # Final model using all data
    regressor3 = LinearRegression(fit_intercept=False)
    regressor3.fit(x, y)
    pred = regressor3.predict(x)
    # print(param_list)
    # with np.printoptions(linewidth=200):
    #     print(regressor3.coef_)
    if round is not None:
        rounded_coefs = np.round(regressor3.coef_, round)

    results.coefs_ols = str(list(rounded_coefs))
    predicted[OLS] = pred

    #print("Coefficients constrained to non-negative values, least-squares method")

    lb = 0
    ub = np.Inf
    res = lsq_linear(x, y, bounds=(lb, ub))

    # Round the coefficients if requested to.
    # print(param_list)
    if round is not None:
        res.x = np.round(res.x, round)

    results.coefs_nnls = str(list(res.x))
    predicted[NNLS] = np.dot(x, res.x)
    for i in [NNLS, OLS]:
        if i == NNLS:
            results.outliers_nnls = str([(bench, predicted, actual, 100 * (predicted - actual) / actual) for (bench, predicted, actual) in zip(df.loc[:, 'Bench'], predicted[i], y) if abs(predicted - actual) / actual > threshold])

            # Determine and print mean(abs(relative error)).
            mean_abs_percentage_error = np.round((mean_absolute_error(
                y / y, predicted[i] / y) * 100.0), round)
            results.mean_abs_percentage_error_nnls = mean_abs_percentage_error

            # Determine and print mean(percentage error).
            percentage_error_vect = predicted[i] / y - y / y
            mean_percentage_error = (percentage_error_vect).mean() * 100.0
            results.mean_percentage_error_nnls = mean_percentage_error
            results.percentage_error_vect_nnls = str([np.round(num, round+5) for num in list(percentage_error_vect)])


            # Determine and print the median error.
            results.median_percentage_error_nnls = np.round(np.median(
                percentage_error_vect) * 100.0, round)
            # print("MEDIAN(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), median_percentage_error[i] * 100.0))

            # Determine and print root of mean square relative error.
            mean_squared_RE = mean_squared_error(y / y, predicted[i] / y)
            results.rmsre_nnls = np.round(np.sqrt(mean_squared_RE) * 100.0, round)
            # print("rootMSRE_%s = %.5f%%" % (get_mode_name(i), rmsre[i] * 100.0))

            results.stddev_abs_percentage_error_nnls = np.sqrt(mean_squared_error(np.full(y.shape, mean_abs_percentage_error), predicted[i]/y - np.full(y.shape, 1.0)))
            # print("STDDEV(MAPE_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_abs_percentage_error[i] * 100.0))

            results.stddev_relative_error_nnls = np.sqrt(mean_squared_error(np.full(y.shape, mean_percentage_error), predicted[i]/y - np.full(y.shape, 1.0)))
            # print("STDDEV(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_relative_error[i] * 100.0))

            mse = mean_squared_error(y, predicted[i])
            rmse = np.sqrt(mse)
            r2 = r2_score(y, predicted[i])
            results.rmse_nnls = np.round(rmse, round)
            results.r2_score_nnls = r2
            # print(("RMSE Score %s:" % get_mode_name(i)) + str(rmse))
            # print(("R2 Score %s:" % get_mode_name(i)) + str(r2_score(y, predicted[i])))

            # print("List of %d/%d outliers using %s at threshold %.2f%% (predicted, actual, error in %%):" %
            #       (len(list(filter(None, outliers[i]))), len(outliers[i]), get_mode_name(i), threshold * 100.0))
            # print("=================================================")
            # [print("%s: %.9f, %.9f, %5.2f%%" % elt)
            #  if elt else None for elt in outliers[i]]
        else:
            results.outliers_ols = str([(bench, predicted, actual, 100 * (predicted - actual) / actual) for (bench, predicted, actual) in zip(df.loc[:, 'Bench'], predicted[i], y) if abs(predicted - actual) / actual > threshold])

            # Determine and print mean(abs(relative error)).
            mean_abs_percentage_error = np.round(mean_absolute_error(
                y / y, predicted[i] / y) * 100.0, round)
            results.mean_abs_percentage_error_ols = np.round(mean_abs_percentage_error, round)
            # print("MAPE_%s = %.5f%%" %
            #       (get_mode_name(i), mean_abs_percentage_error[i] * 100.0))

            # Determine and print mean(percentage error).
            percentage_error_vect = predicted[i] / y - y / y

            mean_percentage_error = (
                percentage_error_vect).mean() * 100.0
            results.mean_percentage_error_ols = np.round(mean_percentage_error, round)
            results.percentage_error_vect_ols = str([np.round(num, round+5) for num in list(percentage_error_vect)])

            # print("MEAN(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), mean_percentage_error[i] * 100.0))

            # Determine and print the median error.
            results.median_percentage_error_ols = np.round(np.median(
                percentage_error_vect) * 100.0, round)
            # print("MEDIAN(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), median_percentage_error[i] * 100.0))

            # Determine and print root of mean square relative error.
            mean_squared_RE = mean_squared_error(y / y, predicted[i] / y)
            results.rmsre_ols = np.round((np.sqrt(mean_squared_RE) * 100.0), round)
            # print("rootMSRE_%s = %.5f%%" % (get_mode_name(i), rmsre[i] * 100.0))

            results.stddev_abs_percentage_error_ols = np.sqrt(mean_squared_error(np.full(y.shape, mean_abs_percentage_error), predicted[i]/y - np.full(y.shape, 1.0)))
            # print("STDDEV(MAPE_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_abs_percentage_error[i] * 100.0))

            results.stddev_relative_error_ols = np.sqrt(mean_squared_error(np.full(y.shape, mean_percentage_error), predicted[i]/y - np.full(y.shape, 1.0)))
            # print("STDDEV(percentage_error_%s) = %.5f%%" %
            #       (get_mode_name(i), stddev_relative_error[i] * 100.0))

            mse = mean_squared_error(y, predicted[i])
            rmse = np.sqrt(mse)
            r2 = r2_score(y, predicted[i])
            results.rmse_ols = np.round(rmse, round)
            results.r2_score_ols = r2
            # print(("RMSE Score %s:" % get_mode_name(i)) + str(rmse))
            # print(("R2 Score %s:" % get_mode_name(i)) + str(r2_score(y, predicted[i])))

            # print("List of %d/%d outliers using %s at threshold %.2f%% (predicted, actual, error in %%):" %
            #       (len(list(filter(None, outliers[i]))), len(outliers[i]), get_mode_name(i), threshold * 100.0))
            # print("=================================================")
            # [print("%s: %.9f, %.9f, %5.2f%%" % elt)
            #  if elt else None for elt in outliers[i]]
    results.results_timestamp = timezone.now()
    return results
