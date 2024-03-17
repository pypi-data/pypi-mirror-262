# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from surfaces_dashboard.page_setup import page_setup

page_setup()

import streamlit as st

from surfaces import mathematical_functions_2d
from surfaces_dashboard.test_functions import TestFunction2dDetailsPage


test_functions_2d = {}
for mathematical_function_2d in mathematical_functions_2d:
    test_functions_2d[mathematical_function_2d.name] = mathematical_function_2d()


test_function_key = st.sidebar.selectbox(
    "Select test function", list(test_functions_2d.keys())
)


TestFunction2dDetailsPage(test_functions_2d[test_function_key]).run()
