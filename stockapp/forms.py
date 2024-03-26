from typing import Any
from django import forms
from django.core.validators import RegexValidator
from datetime import datetime


ticker_validators = [
    RegexValidator(
        r"^[A-z\.:\-]{3,20}$", 
        message='Please Enter a valid symbol like: "aapl", "amzn" , "tsla"'
    )
]
years: range = range(2000, 2025)


class StockForm(forms.Form):
    ticker_symbol = forms.CharField(
        max_length=20, 
        min_length=3, 
        validators=ticker_validators, 
        label="Ticker Symbol"
    )
    start_date = forms.DateTimeField(
        label="Start Date", 
        required=False,
        widget=forms.widgets.SelectDateWidget(years=years),
    )
    end_date = forms.DateTimeField(
        label="End Date", 
        required=False,
        widget=forms.widgets.SelectDateWidget,
    )


