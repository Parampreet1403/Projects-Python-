# Parampreet Singh - 22/06/20
# Time Series Analysis in Python

"""
Time Series Analysis:
- Only one variable which is time
- Componenets: Trend, Seasonality, Irregularity, Cyclic


Stationarity:
- constant mean
- constant variance (distance from mean)
- autocovariance


ARIMA Model: (two separate models brought together)
- AR: Auto Regressive
- I: Integration
- MA: Moving Average

3 parameters (P, d, Q)
P = autoregressive lags (Partial auto-correlation graph)
d = order of differentiation
Q = moving average (auto-correlation plot)

"""

"""
Problem: Build a model to forecast the demand (passenger traffic) in Airplanes. 
The data is classifies in date/time and the passengers travelling per month.
"""
