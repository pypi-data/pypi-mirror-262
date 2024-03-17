# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from surfaces_dashboard.page_setup import page_setup

page_setup()


import streamlit as st
from surfaces.mathematical_functions import (
    RastriginFunction,
    GramacyAndLeeFunction,
    HimmelblausFunction,
)

from test_functions import TestFunction1dDetailsPage, TestFunction2dDetailsPage


def vertical_space(pos, n=3):
    for _ in range(n):
        pos.write("")


col1, col2 = st.columns((1, 1))


test_function_1d = RastriginFunction(n_dim=1)


TestFunction2dDetailsPage(HimmelblausFunction()).display_surface_plot(col2)

vertical_space(col1)
col1.subheader("About this page", divider=True)

vertical_space(col1)
col1.subheader("Mathematical Test functions", divider=True)
