import streamlit as st
import pandas as pd

def carregar_dados():
    df = pd.read_excel("Tabela_Spice.xlsx")
    return df
#Cabeçalhos do sistemas

st.set_page_config(
                    page_title="Calculadora de Frete",
                    layout="wide", 
                    page_icon="cotralti_logo.png",
                    #initial_sidebar_state="collapsed" # inicia com barra de filtros fechada
)

st.header("Calculadora de :blue[Frete] ", divider='green')

#df = pd.DataFrame(TabelaSpice)
df = carregar_dados()


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

  
def calcular_frete(rota_digitada, peso_digitado, ):
    # Filtrar a linha correspondente ao código fornecido
   
    df_filtro = df[df['Código'] == rota_digitada]
    
    if df_filtro.empty:
        return "Código não encontrado."
    
   
     # Obter os valores mínimos e as faixas de peso
    peso_minimo = df_filtro['Peso_Mínimo'].values[0]
    frete_minimo = df_filtro['Frete_Mínimo'].values[0]
    
    
    if rota_digitada == 'ARCRS05' or rota_digitada == 'ARCRS06' or rota_digitada == 'ARCSC07':
    
        if peso_digitado <= peso_minimo:
            return frete_minimo
        elif peso_digitado > peso_minimo and peso_digitado <= 1000:
            return df_filtro['Até_1.000'].values[0], f"Faixa de Peso de 1000 kg"
        elif peso_digitado >= 1001 and peso_digitado <= 3000:
            return df_filtro['1.001_3.000'].values[0]
        elif peso_digitado >=3001 and peso_digitado <= 6000:
            return df_filtro['3.001_6.000'].values[0]
        elif peso_digitado >=6001 and peso_digitado <= 13000:
            return df_filtro['6.001_13.000'].values[0]
        else:
            return df_filtro['Acima_13.001'].values[0] 
    
    if rota_digitada != 'ARCRS05' or rota_digitada != 'ARCRS06' or rota_digitada != 'ARCSC07':
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
       
       if st.button("Cᥲᥣᥴᥙᥣᥲr Frᥱtᥱ",help="Favor incluir os dados nos campos!", type="primary"):

        
        valor_frete = calcular_frete(rota_digitada , peso_digitado)
        fretepeso = (valor_frete)
        regiao = df_filtro["Destino_Regiões"].values[0]
        taxanf = df_filtro["Taxa_NFE"].values[0]
        tipo = df_filtro["Tipo"].values[0]
        adv = df_filtro["ADV(%)"].values[0]
                    
        st.divider()
        
        st.success("𝖢𝗈𝗇𝗌𝖾𝗀𝗎𝗂𝗆𝗈𝗌 𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗋 𝖺 𝗌𝗎𝖺 𝗌𝗈𝗅𝗂𝖼𝗂𝗍𝖺𝖼̧𝖺̃𝗈 𝗌𝗈𝖻𝗋𝖾 𝗈 𝖿𝗋𝖾𝗍𝖾.")
        coluna_esquerda , coluna_meio  = st.columns([2, 1])  
                
        coluna_meio.metric(f"**A Tabela escolhida é** ",f'{rota_digitada}')
        coluna_esquerda.metric("𝗢 𝘃𝗮𝗹𝗼𝗿 𝗱𝗼 𝗙𝗿𝗲𝘁𝗲 𝗥𝗼𝘁𝗮 𝗲́",f'R$ {fretepeso:,.2f} reais')
       
        st.divider()
        
        st.write("❶ O frete total é calculado: ( **Frete Rota + Taxa NF + ADValorem + Icms )**.")
        st.write(f"❷ O Destino é as  **{regiao}** .")
        st.write(f"❸ O valor da Emissão das Notas Fiscais é de **R$ {taxanf:.2f} reais**.")
        st.write(f"❹ O Advalorem é de  **{adv:,.2f}%**.")
        st.write(f"❺ O Icms é de **RJ x RJ = 20%** , **RJ x ( SP, MG, PR, SC e RS ) = 12%** .")
        st.write(f"❻ O Tipo da Carga é **{tipo}**.")
        st.divider()
        st.write("""
         &copy; 2024 - Luis Felipe A. David. Todos os direitos reservados
         """) 
else:
    st.button("Calcular Frete",disabled=True)
    
    st.write("""
         &copy; 2024 - Luis Felipe A. David. Todos os direitos reservados
         """)
