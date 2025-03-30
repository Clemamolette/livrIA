#!/bin/bash
export PYTHONPATH=$(pwd)
streamlit run src/app.py --theme.primaryColor="rgb(203, 166, 247)" --theme.backgroundColor="rgb(61, 15, 125)" --theme.textColor="rgb(205, 214, 244)" --theme.base="dark"