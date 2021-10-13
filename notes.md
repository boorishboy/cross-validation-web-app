# Cross validation web app for RISC-V time modeling using Django

## Idea
Basic idea is to create a tool to interactively analyze and present ML model. In this particular case it will be cross validation for RISC-V time consumption (and optionally energy). 
## Resources

## What needs to be done

## Changes done

1. Display_scores wrong variable and deleted ***nmse_scores*** as it duplicates with ***scores*** variable
### old
 ```python
regressor2 = LinearRegression(fit_intercept=False)
nmse_scores = cross_val_score(regressor2, x,y, scoring="neg_mean_squared_error", cv=10)
scores = cross_val_score(regressor2, x,y, scoring="neg_mean_squared_error", cv=10)
try:
    rmse_scores = np.sqrt(-scores)
except:
    print("### np.sqrt(-scores) failed, scores = " + str(scores))
display_scores(scores)
```
### new
```python
regressor2 = LinearRegression(fit_intercept=False)
scores = cross_val_score(regressor2, x,y, scoring="neg_mean_squared_error", cv=10)
try:
    rmse_scores = np.sqrt(-scores)
except:
    print("### np.sqrt(-scores) failed, scores = " + str(scores))
display_scores(rmse_scores)
```

2.Fixed ***print*** function in line 83

### old
```python
x = df.loc[:,param_list].values
print(y)
```

### new
```python
x = df.loc[:,param_list].values
print(x)
```
