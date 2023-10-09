import datetime

import plotly.graph_objs as go
import requests
import streamlit as st
import pandas as pd
API_URL = "http://127.0.0.1:8000/predict"

MIN_DATE = datetime.date(2021, 8, 1)
MAX_DATE = datetime.date(2030, 12, 1)


def main():

    model = st.selectbox(
        "Please choose forecasting model", ("SARIMA", "Cat Boost", "Prophet")
    )

    start_date = st.date_input(
        "Start date", min_value=MIN_DATE, max_value=MAX_DATE, value=MIN_DATE
    )
    end_date = st.date_input(
        "End date", min_value=MIN_DATE, max_value=MAX_DATE, value=MAX_DATE
    )

    if start_date <= end_date:
        st.success(
            f"Selected start date: `{start_date}`\n\nSelected end date:`{end_date}`"
        )
    else:
        st.error("Error: End date must be after start date.")
    

    fig = go.Figure()

    if st.button("Predict"):
        dates = pd.date_range(start_date,end_date,freq='M').to_list()
        params = {"model": model, "start_date": start_date.strftime('%Y-%m-%d'), "end_date":end_date.strftime('%Y-%m-%d')}

        try:
            response = requests.post(API_URL, json=params)
            response.raise_for_status()

            predictions_json = response.json()
            predictions = predictions_json["predictions"]


            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=predictions,
                    name="Predicted",
                )
            )
            fig.update_layout(title=f"{model} Web Traffic")
            st.plotly_chart(fig)

        except requests.exceptions.RequestException as e:
            st.error(f"Error occurred while making the request: {e}")


if __name__ == "__main__":
    main()