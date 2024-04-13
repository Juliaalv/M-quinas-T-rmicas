import streamlit as st
import plotly.graph_objects as go
import numpy as np

import sys
sys.path.append('utils')  

from calculos import main
from pv import pv


# Execução do programa
if __name__ == "__main__":
    st.title('Simulação Motor Diesel')
    pv()
    main()

