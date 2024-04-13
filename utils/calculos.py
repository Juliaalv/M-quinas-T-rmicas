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
    
    # Valores de velocidade angular (RPM) para o gráfico
    omega_values = np.linspace(1000, 6000, 100)

    # Diâmetro do pistão em metros
    diametro_pistao_128 = 128 / 1000  # Convertendo para metros
    
    # Calculando as curvas para o diâmetro do pistão de 128 mm
    torque_values_128 = calcular_torque(omega_values, n_cilindros, diametro_pistao_128, V_cilindro, taxa_compressao, R, gamma, P_atm, T_amb)
    potencia_values_128 = calcular_potencia(torque_values_128, omega_values)
    consumo_especifico_values_128 = calcular_consumo_especifico(torque_values_128, omega_values, n_cilindros, V_cilindro, taxa_compressao, R, gamma, P_atm, T_amb)
    figuras_128 = plotar_graficos(omega_values, torque_values_128, potencia_values_128, consumo_especifico_values_128, diametro_pistao_128)

    # Apresentando os gráficos para o diâmetro do pistão de 128 mm no Streamlit
    st.plotly_chart(figuras_128[0], use_container_width=True)
    st.plotly_chart(figuras_128[1], use_container_width=True)
    st.plotly_chart(figuras_128[2], use_container_width=True)
    
    # Lista de diâmetros de pistão em metros
    diametros_pistao = [150, 170]
    # Gerando amostras para o pistão no intervalo de 150 a 170 mm
    amostras_diametro_pistao = np.linspace(diametros_pistao[0], diametros_pistao[1], int(((diametros_pistao[1] - diametros_pistao[0]) / 2) + 1))
    # Convertendo os valores das amostras em metros
    amostras_diametro_pistao_m = amostras_diametro_pistao / 1000
    # Rotação fixa
    omega_value2 = 3000
    # Listas para armazenar os valores de torque, potência e consumo específico
    torque_values = []
    powers_values = []
    ces_values = []

    # Cálculo dos valores de torque, potência e consumo específico para cada diâmetro de pistão
    for diametro_pistao in amostras_diametro_pistao_m:
        V_comb = V_cilindro / (taxa_compressao - 1)
        m_ar = (P_atm * V_comb) / (R * T_amb)
        
        torque = m_ar * (gamma * R * T_amb) * (1 - (1 / (omega_value2 * n_cilindros * V_comb))) * ((diametro_pistao) / 2)**2 * np.pi
        torque_values.append(torque)

        power = (torque * omega_value2 * 2 * np.pi / 60) / 1000
        powers_values.append(power)

        ces = (m_ar * gamma * R * T_amb) / (power + 1e-10)
        ces_values.append(ces)

    # Plotando as figuras
    fig_torque = go.Figure()
    fig_torque.add_trace(go.Scatter(x=amostras_diametro_pistao_m * 1000, y=torque_values, mode='lines', name='Torque'))
    fig_torque.update_layout(title='Curva de Torque', xaxis_title='Diâmetro do Pistão (mm)', yaxis_title='Torque (N.m)', height=400)

    fig_potencia = go.Figure()
    fig_potencia.add_trace(go.Scatter(x=amostras_diametro_pistao_m * 1000, y=powers_values, mode='lines', name='Potência'))
    fig_potencia.update_layout(title='Curva de Potência', xaxis_title='Diâmetro do Pistão (mm)', yaxis_title='Potência (kW)', height=400)

    fig_consumo = go.Figure()
    fig_consumo.add_trace(go.Scatter(x=amostras_diametro_pistao_m * 1000, y=ces_values, mode='lines', name='Consumo Específico'))
    fig_consumo.update_layout(title='Curva de Consumo Específico', xaxis_title='Diâmetro do Pistão (mm)', yaxis_title='Consumo Específico (kg/W.s)', height=400)

    # Apresentando os gráficos no Streamlit
    st.plotly_chart(fig_torque, use_container_width=True)
    st.plotly_chart(fig_potencia, use_container_width=True)
    st.plotly_chart(fig_consumo, use_container_width=True)


