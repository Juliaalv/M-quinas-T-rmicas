
#Bibliotecas Necessárias
import streamlit as st
import sys
sys.path.append('utils')  

from calculos import main
from pv import pv


# Execução do programa
if __name__ == "__main__":
    st.title('Simulação Motor Diesel')
    pv()
    main()

