# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from surfaces_dashboard.page_setup import page_setup

page_setup()

import streamlit as st

from surfaces import mathematical_functions_1d
from surfaces_dashboard.test_functions import TestFunction1dDetailsPage


test_functions_1d = {}
for mathematical_function_2d in mathematical_functions_1d:
    test_functions_1d[mathematical_function_2d.name] = mathematical_function_2d()


test_function_key = st.sidebar.selectbox(
    "Select test function", list(test_functions_1d.keys())
)


TestFunction1dDetailsPage(test_functions_1d[test_function_key]).run()
