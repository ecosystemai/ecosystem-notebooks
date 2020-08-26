#!/bin/sh
# pip install jupyter notebook
pip install jupyter_contrib_nbextensions
pip install jupyterthemes
jupyter contrib nbextension install --user
jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable splitcell/splitcell
jupyter nbextension enable toc2/main
jupyter nbextension enable hide_input/main
jt -t chesterish -T -N