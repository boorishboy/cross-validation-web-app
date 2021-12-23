# Web application and API for machine learning data analysis
## Installation
1. ### Clone git repo
```git clone https://github.com/boorishboy/cross-validation-web-app.git```

2. ### Install ```virtualenv```
```pip install virtualenv```

3. ### Create virtual environment
```python3 -m venv venv```

4. ### Activate virtuall environment
```source venv/bin/activate```

5. ### Install requirements
```pip3 install -r backend/server/requirements.txt```

6. ### Make database migrations in ```backend/server```
```python3 manage.py makemigrations MyAPI```  
```python3 manage.py migrate```

7. ### Run development server (from ```backend/server/```)
```python3 manage.py runserver```

## Run via command line
```curl -F "inputFile=@/Users/boorish/Desktop/data-HW-and-TL.csv" -F "paramList=Executed insns (no MULS), MULS insns, Taken branches, RAM data reads, RAM writes, Flash data reads, Flash insn reads, BL insns, PUSH/POP PC/LR" -F 'targetColumn=HW Cycles (IT adjusted)' -F "round=5" -F "threshold=5" localhost:8000/api/input/
```

## UI pictures
1. Home ![home](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/home.png)
2. New Run ![new-run](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/new%20run%20input.png)
3. Dashboard ![dashboard](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/dashboard%20initial.png)
4. Dashboard Dropdown ![dashboard-dropdown](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/dashboard%20dropdown.png)
5. Dashboard Data Validation ![dashboard-data-val](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/dashboard%20data%20validation.png)
6. Dashboard Results ![dashboard-results-1](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/dashboard%20results%201.png)
7. Dashboard Results ![dashboard-results-2](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/dashboard%20results%202.png)
8. Dashboard Raw Data ![dashboard-results-2](https://github.com/boorishboy/cross-validation-web-app/blob/main/pics/dashboard%20raw%20data.png)
