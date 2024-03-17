# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from surfaces_dashboard.page_setup import page_setup

page_setup()

import streamlit as st

from surfaces import mathematical_functions_nd
from surfaces_dashboard.test_functions import TestFunctionNdDetailsPage


test_functions_nd = {}
for mathematical_function_nd in mathematical_functions_nd:
    test_functions_nd[mathematical_function_nd.name] = mathematical_function_nd


test_function_key = st.sidebar.selectbox(
    "Select test function", list(test_functions_nd.keys())
)


TestFunctionNdDetailsPage(test_functions_nd[test_function_key]).run()
