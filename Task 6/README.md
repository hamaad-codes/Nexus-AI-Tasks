Sales Forecasting – Task 6
📌 Project Overview

The goal of this project is to build a time series forecasting model that predicts sales for the next 30 days.
The model is trained on the Superstore Sales Dataset using the SARIMA algorithm.
The results are visualized by plotting both historical sales and future forecasts on a single graph.

⚙️ Steps Performed

Data Preparation

Loaded the dataset and set Order Date as the index.

Handled missing values and applied differencing to make the data stationary.

Model Training

Trained the SARIMA (Seasonal ARIMA) model on historical sales data.

Tuned model parameters (p, d, q) and seasonal parameters (P, D, Q, s).

Forecasting

Used the trained model to forecast sales for the next 30 days.

Visualization

Plotted both historical sales and forecasted sales on a single graph to compare them.

How to Run

Install the required libraries:

pip install pandas matplotlib statsmodels scikit-learn


Run the notebook:

Open Jupyter Notebook and run the task6.ipynb.

Expected Output

After training the model, you will get a graph showing:

Blue line: Historical sales data

Red line: Forecast for the next 30 days

The notebook will also display the SARIMA model summary and performance metrics (RMSE).