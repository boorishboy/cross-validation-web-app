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


NNLS = 0
OLS = 1

def get_mode_name(mode):
    '''Return name of the current mode.'''
    return ('OLS' if i == OLS else 'NNLS')

def get_file_label(mode):
    '''Return filesystem-friendly name of the regressand field.'''
    return ('Energy' if 'Energy' in mode else 'Cycles')

def display_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())


df = pd.read_csv("stats_and_modeling/COMBINED/48/1/0/data-HW-and-TL.csv")
param_list = ['Executed insns (no MULS)', 'MULS insns', 'Taken branches', 'RAM data reads', 'RAM writes', 'Flash data reads', 'Flash insn reads', 'BL insns', 'PUSH/POP PC/LR']
target_column = 'HW Cycles (IT adjusted)'
adjust = 1.0
round = 5
threshold = 5.0 / 100

y = df.loc[:,target_column].values
# Adjust the regressand.
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
            print((y - (df.loc[:,param].values * param_value_dict[param]))/y)
            print('')
            y = y - (df.loc[:,param].values * param_value_dict[param])
        else:
            unconstrained_params.append(param)
    # Reset param list to the free-running parameters only.
    param_list = unconstrained_params
else:
    pass

x = df.loc[:,param_list].values
regressor = LinearRegression(fit_intercept=False)
rkf = RepeatedKFold(n_splits=10, n_repeats=1, random_state=None)
scrs = []
count = 0
for train_index, test_index in rkf.split(x):
    clone_regressor = clone(regressor)
    #print("Train:", train_index, "\nValidation:", test_index)
    X_train, X_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    clone_regressor.fit(X_train,y_train)
    y_pred = clone_regressor.predict(X_test)
    mse = mean_squared_error(y_test,y_pred)
    rmse = np.sqrt(mse)
    scrs.append(rmse)
    count = count + 1;

scrs_array = np.asarray(scrs)
display_scores(scrs_array)

# Evaluate score by cross validation
regressor2 = LinearRegression(fit_intercept=False)
scores = cross_val_score(regressor2, x, y, scoring="neg_mean_squared_error", cv=10)
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
from scipy.optimize import lsq_linear

lb = 0
ub = np.Inf
res = lsq_linear(x, y, bounds=(lb, ub))

# Round the coefficients if requested to.
#print(param_list)
if round is not None:
    res.x = np.round(res.x, round)

#with np.printoptions(linewidth=200):
#    print(res.x)

coefs[NNLS] = res.x
predicted[NNLS] = np.dot(x, res.x)

mean_abs_percentage_error = [None] * 2
percentage_error_vect = [None] * 2
mean_percentage_error = [None] * 2
median_percentage_error = [None] * 2
mean_squared_RE = [None] * 2
rmsre = [None] * 2
stddev_abs_percentage_error = [None] * 2
stddev_relative_error = [None] * 2
mse = [None] * 2
rmse = [None] * 2

for i in [NNLS, OLS]:
    outliers[i] = [ (bench, predicted, actual, 100*(predicted - actual)/actual) if abs(predicted - actual)/actual > threshold else None for (bench, predicted, actual) in zip(df.loc[:,'Bench'], predicted[i], y) ]

    # Determine and print mean(abs(relative error)).
    mean_abs_percentage_error[i] = mean_absolute_error(y/y, predicted[i]/y)
    print ("MAPE_%s = %.5f%%" % (get_mode_name(i), mean_abs_percentage_error[i] * 100.0))

    # Determine and print mean(percentage error).
    percentage_error_vect[i] = predicted[i]/y - y/y
    mean_percentage_error[i] = (percentage_error_vect[i]).mean()
    print ("MEAN(percentage_error_%s) = %.5f%%" % (get_mode_name(i), mean_percentage_error[i] * 100.0))

    # Determine and print the median error.
    median_percentage_error[i] = np.median(percentage_error_vect[i])
    print ("MEDIAN(percentage_error_%s) = %.5f%%" % (get_mode_name(i), median_percentage_error[i] * 100.0))

    # Determine and print root of mean square relative error.
    mean_squared_RE[i] =  mean_squared_error(y/y, predicted[i]/y)
    rmsre[i] =  np.sqrt(mean_squared_RE[i])
    print ("rootMSRE_%s = %.5f%%" % (get_mode_name(i), rmsre[i] * 100.0))

    stddev_abs_percentage_error[i] = np.sqrt(mean_squared_error(np.full(y.shape, mean_abs_percentage_error[i]), predicted[i]/y - np.full(y.shape, 1.0)))
    print ("STDDEV(MAPE_%s) = %.5f%%" % (get_mode_name(i), stddev_abs_percentage_error[i] * 100.0))

    stddev_relative_error[i] = np.sqrt(mean_squared_error(np.full(y.shape, mean_percentage_error[i]), predicted[i]/y - np.full(y.shape, 1.0)))
    print ("STDDEV(percentage_error_%s) = %.5f%%" % (get_mode_name(i), stddev_relative_error[i] * 100.0))

    mse[i] = mean_squared_error(y, predicted[i])
    rmse[i] = np.sqrt(mse[i])
    print (("RMSE Score %s:" % get_mode_name(i)) + str(rmse))
    print (("R2 Score %s:" % get_mode_name(i)) +  str(r2_score(y, predicted[i])))

    print("List of %d/%d outliers using %s at threshold %.2f%% (predicted, actual, error in %%):" % (len(list(filter(None, outliers[i]))), len(outliers[i]), get_mode_name(i), threshold*100.0))
    print("=================================================")
    [ print("%s: %.9f, %.9f, %5.2f%%" % elt) if elt else None for elt in outliers[i] ]
