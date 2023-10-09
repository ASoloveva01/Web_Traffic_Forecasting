import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
import joblib
from catboost import CatBoostRegressor
app = FastAPI()
from prophet.serialize import model_from_json
import uvicorn
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from helpers import datetime_features
class TrafficRequest(BaseModel):
    model: str
    start_date: str
    end_date: str
MODELS_FILE_PATHS = {
    'SARIMA': '../models/sarima.pkl',
    'CatBoost': '../models/catboost',
    'Prophet': '../models/prophet.json'
}

@app.post('/predict')
async def predict(traffic_request: TrafficRequest):
    model = traffic_request.model
    start_date = traffic_request.start_date
    end_date = traffic_request.end_date
    dates = pd.date_range(start_date,end_date,freq='M')
    predictions = None
    if model == 'SARIMA':
        model = joblib.load(MODELS_FILE_PATHS['SARIMA'])
        predictions = model.predict(start_date=start_date, end_date=end_date).tolist()
    elif model == 'Cat Boost':
        model = CatBoostRegressor()
        model.load_model(MODELS_FILE_PATHS['CatBoost'])
        
        dates_df = pd.DataFrame(dates, columns=['Date'])
        dates_df['Date'] = pd.to_datetime(dates_df['Date'], format='%Y-%m-%d')
        dates_df = dates_df.set_index('Date')
        datetime_features(dates_df)
        predictions = model.predict(dates_df).tolist()
    else:
        with open(MODELS_FILE_PATHS['Prophet'], 'r') as fin:
            model = model_from_json(fin.read())
        future_df = pd.DataFrame({'ds': dates})
        predictions = model.predict(future_df)['yhat'].tolist()
    

    return {'predictions': predictions}

if __name__ == '__main__':
    uvicorn.run('main:app', host='http://127.0.0.1', port=8000, reload=True)