import numpy as np
import streamlit as st
import plotly.graph_objects as go


# Função para calcular o torque
def calcular_torque(omega_values, n_cil, diametro_pistao, V_cilindro, taxa_compressao, R, gamma, P_atm, T_amb):
    V_comb = V_cilindro / (taxa_compressao - 1)
    m_ar = (P_atm * V_comb) / (R * T_amb)
    torque_values = m_ar * (gamma * R * T_amb) * (1 - (1 / (omega_values * n_cil * V_comb))) * (diametro_pistao / 2)**2 * np.pi
    return torque_values

def calcular_potencia(torque_values, omega_values):
    return (torque_values * omega_values * 2 * np.pi / 60) / 1000

# Função para calcular o consumo específico
def calcular_consumo_especifico(torque_values, omega_values, n_cil, V_cilindro, taxa_compressao, R, gamma, P_atm, T_amb):
    V_comb = V_cilindro / (taxa_compressao - 1)
    m_ar = (P_atm * V_comb) / (R * T_amb)
    return (m_ar * gamma * R * T_amb) / (calcular_potencia(torque_values, omega_values) + 1e-10)


# Função para gerar os gráficos
def plotar_graficos(omega_values, torque_values, potencia_values, consumo_especifico_values, diametro_pistao):
    fig_torque = go.Figure()
    fig_torque.add_trace(go.Scatter(x=omega_values, y=torque_values, mode='lines', name='Torque'))
    fig_torque.update_layout(title=f'Curva de Torque (Diâmetro do Pistão: {diametro_pistao * 1000} mm)',
                             xaxis_title='RPM', yaxis_title='Torque (N.m)', height=400)
    
    fig_potencia = go.Figure()
    fig_potencia.add_trace(go.Scatter(x=omega_values, y=potencia_values, mode='lines', name='Potência'))
    fig_potencia.update_layout(title=f'Curva de Potência (Diâmetro do Pistão: {diametro_pistao * 1000} mm)',
                               xaxis_title='RPM', yaxis_title='Potência (kW)', height=400)

    fig_consumo = go.Figure()
    fig_consumo.add_trace(go.Scatter(x=omega_values, y=consumo_especifico_values, mode='lines', name='Consumo Específico'))
    fig_consumo.update_layout(title=f'Curva de Consumo Específico (Diâmetro do Pistão: {diametro_pistao * 1000} mm)',
                               xaxis_title='RPM', yaxis_title='Consumo Específico (kg/W.s)', height=400)
    
    return fig_torque, fig_potencia, fig_consumo

# Função base
def main():
    
    # Volume do cilindro em litros
    V_cilindro = 24.2  
    # Taxa de compressão
    taxa_compressao = 14 
    # Constante específica dos gases em J/(kg·K)
    R = 287 
    # Razão de calor específico para ar
    gamma = 1.4  
    # Razão de calor específico para ar
    P_atm = 1.01325 * 10**5  
    # Razão de calor específico para ar
    T_amb = 25 + 273.15  
    # Número de cilindros
    n_cilindros = 12  
    
    # Valores de velocidade angular (RPM)
    omega_values = np.linspace(1000, 6000, 100)

    diametros_pistao = [150 / 1000, 170 / 1000]  # Convertendo para metros
    
    
    for diametro_pistao in diametros_pistao:
        torque_values = calcular_torque(omega_values, n_cilindros, diametro_pistao, V_cilindro, taxa_compressao, R, gamma, P_atm, T_amb)
        potencia_values = calcular_potencia(torque_values, omega_values)
        consumo_especifico_values = calcular_consumo_especifico(torque_values, omega_values, n_cilindros, V_cilindro, taxa_compressao, R, gamma, P_atm, T_amb)
        figuras = plotar_graficos(omega_values, torque_values, potencia_values, consumo_especifico_values, diametro_pistao)
        
        # Apresentando os gráficos no Streamlit
        st.plotly_chart(figuras[0], use_container_width=True)
        st.plotly_chart(figuras[1], use_container_width=True)
        st.plotly_chart(figuras[2], use_container_width=True)