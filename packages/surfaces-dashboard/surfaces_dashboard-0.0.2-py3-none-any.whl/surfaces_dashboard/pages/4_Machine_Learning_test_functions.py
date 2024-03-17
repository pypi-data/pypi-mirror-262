# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from surfaces_dashboard.page_setup import page_setup

page_setup()

import streamlit as st

from surfaces import machine_learning_functions
from surfaces_dashboard.test_functions import TestFunctionMlDetailsPage


test_functions_ml = {}
for mathematical_function_ml in machine_learning_functions:
    test_functions_ml[mathematical_function_ml.name] = mathematical_function_ml()


test_function_key = st.sidebar.selectbox(
    "Select test function", list(test_functions_ml.keys())
)


TestFunctionMlDetailsPage(test_functions_ml[test_function_key]).run()
