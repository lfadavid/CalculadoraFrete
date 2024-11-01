import streamlit as st
import pandas as pd
from model import TabelaSpice

st.set_page_config(
                    page_title="Calculadora de Frete",
                    layout="wide", 
                    page_icon="cotralti_logo.png",
                    #initial_sidebar_state="collapsed" # inicia com barra de filtros fechada
)

#Cabeçalhos do sistemas

st.header("Calculadora de :blue[Frete] ", divider='green')

#Sidebar e seus comandos
with st.sidebar:
    st.sidebar.image("cotralti_logo.png",width=80)
    st.sidebar.markdown("""
                    #### Desenvolvido  por http://cotralti.com.br
                    """)
    st.write("""
              ###### &copy; 2024 - Luis Felipe A. David - Todos os direitos reservados
         """)
    st.text("Fonte: Tabela Spice.")

#Banco de dados com os valores usando lista ao inves de planilha tiramdo da model

#df = pd.DataFrame(TabelaSpice)
df = pd.read_excel("Tabela_Spice.xlsx")

#Inserindo as colunas na tela
coluna_esquerda , coluna_meio , coluna_direita = st.columns([1, 1, 1])

peso_digitado = coluna_esquerda.number_input(label="Digite o peso em Kg", min_value=0.0, placeholder="Digite o valor do peso", value=None)

rota_digitada = coluna_meio.selectbox(
                        key=1,
                        label="Código",
                        options=df["Código"].unique(),
                        placeholder="Selecione a rota desejada",
                        index=None
)

#filtrando pelo codigo

df_filtro = df[df['Código'] == rota_digitada]

  
def calcular_frete(rota_digitada, peso_digitado):
    # Filtrar a linha correspondente ao código fornecido
   
    df_filtro = df[df['Código'] == rota_digitada]
    
    if df_filtro.empty:
        return "Código não encontrado."
    
   
     # Obter os valores mínimos e as faixas de peso
    peso_minimo = df_filtro['Peso_Mínimo'].values[0]
    frete_minimo = df_filtro['Frete_Mínimo'].values[0]

    # Verificar a faixa de peso
    if peso_digitado <= peso_minimo:
        return frete_minimo
    elif peso_digitado > peso_minimo and peso_digitado <= 1000:
        return (df_filtro['Até_1.000'].values[0] /1000) * peso_digitado
    elif peso_digitado >= 1001 and peso_digitado <= 3000:
        return (df_filtro['1.001_3.000'].values[0] /1000) * peso_digitado
    elif peso_digitado >=3001 and peso_digitado <= 6000:
        return (df_filtro['3.001_6.000'].values[0] /1000) * peso_digitado
    elif peso_digitado >=6001 and peso_digitado <= 13000:
        return (df_filtro['6.001_13.000'].values[0] / 1000) * peso_digitado
    else:
        return (df_filtro['Acima_13.001'].values[0] / 1000) * peso_digitado


if peso_digitado is not None and rota_digitada is not None:
       
       if st.button("Calcular Frete",help="Favor incluir os dados nos campos!", type="primary"):

        valor_frete = calcular_frete(rota_digitada , peso_digitado)
        fretepeso = (valor_frete)
        regiao = df_filtro["Destino_Regiões"].values[0]
        taxanf = df_filtro["Taxa_NFE"].values[0]
        adv = df_filtro["ADV(%)"].values[0]
        fretefinal = (fretepeso * 0.12) + (fretepeso * adv) + taxanf + fretepeso
            
        st.divider()
                
        st.success("Conseguimos calcular os seus dados")
        coluna_esquerda , coluna_meio  = st.columns([1, 1])  
                
        coluna_meio.metric(f"**O Frete Total é** ",f'R$ {fretefinal:,.2f} reais')
        coluna_esquerda.metric("O valor do Frete Rota é ",f'R$ {fretepeso:,.2f} reais')
            
        st.write(f"_A Tabela Selecionada é_ **{rota_digitada}**.")
        st.write(f"_O Destino é as_  **{regiao}** .")
        st.write(f"_O valor da Emissão das Notas Fiscais é de_ **R$ {taxanf:.2f} reais**.")
        st.write(f"_O Advalorem é de_  **{adv:,.2f}%**.")
        st.write(f"O Icms é de **12%**.")
        st.divider()
else:
    st.button("Calcular Frete",disabled=True)