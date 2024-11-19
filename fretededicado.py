import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    df = pd.read_excel("FreteDedicado.xlsx")
    return df

st.header("Frete :blue[Dedicado] ", divider='green')

#df = pd.DataFrame(TabelaSpice)
df = carregar_dados()

#Inserindo as colunas na tela
coluna_esquerda , coluna_meio , coluna_direita = st.columns([1, 1, 1])
col1, col2 , col3 = st.columns([1,1,1])


peso_digitado = coluna_esquerda.number_input(label="Digite o peso em Kg", min_value=0.0, placeholder="Digite o valor do peso", value=None)

  
origem_local = coluna_meio.selectbox(
                          key=1,
                          label="Origem Local",
                          options=df['Origem_Local'].unique(),
                          placeholder="Selecione a Origem.",
                          index=None
)

df_filtro_origem = df[df['Origem_Local'] == origem_local]

tipo_carga = coluna_direita.selectbox(
                          key=2,
                          label="Tipo de Carga",
                          options=df_filtro_origem['Tipo'].unique(),
                          placeholder="Selecione a Carga",
                          index=None
)

  #df_filtro_carga = df[df['Tipo'] == tipo_carga]
df_filtro_carga = df_filtro_origem[df['Tipo'] == tipo_carga ]

destino_regiao = col1.selectbox(
                          key=3,
                          label="Região da Entrega",
                          options=df_filtro_carga['Destino_Regiões'],
                          placeholder="Selecione a região",
                          index=None
)
df_filtro_regioes = df_filtro_carga[df['Destino_Regiões'] == destino_regiao]

cliente_destino = col2.selectbox(
                          key=4,
                          label="Cliente",
                          options=df_filtro_regioes['Cliente'],
                          placeholder="Selecione o Cliente",
                          index=None
  )

def calcular_frete(origem_local, peso_digitado ):
   # Filtrar a linha correspondente ao código fornecido
   
    #df_filtro_origem = df[df['Origem_Local'] == origem_local]
    df_filtro_regioes = df_filtro_carga[df['Destino_Regiões'] == destino_regiao]
    if df_filtro_regioes.empty:
        return "Origem não encontrado."
   
    if peso_digitado <= 1000:
            return df_filtro_regioes['Pick_UpAté_1.000kg'].values[0]
    elif peso_digitado >= 1001 and peso_digitado <= 3000:
            return df_filtro_regioes['Leve_Até_3.000kg'].values[0]
    elif peso_digitado >=3001 and peso_digitado <= 6000:
            return df_filtro_regioes['Toco_Até_6.700kg'].values[0]
    elif peso_digitado >=6001 and peso_digitado <= 13000:
            return df_filtro_regioes['Truck_Até_13 Ton'].values[0]
    elif peso_digitado >=13001 and peso_digitado <= 26000:
            return df_filtro_regioes['Carreta_Até_26_Ton'].values[0]
    else:
            return df_filtro_regioes['Carreta LS_>_26.001_Ton'].values[0] 

if peso_digitado is not None and origem_local is not None and tipo_carga is not None and destino_regiao is not None and cliente_destino is not None:
  
 
  if st.button("Cᥲᥣᥴᥙᥣᥲr Frᥱtᥱ",help="Favor incluir os dados nos campos!", type="primary"):
    
    valor_frete = calcular_frete(origem_local , peso_digitado)
    fretepeso  = valor_frete
    prazoentrega = df_filtro_carga['Prazo_Entrega'].values[0]
    cliente = df_filtro_regioes['Cliente'].values[0]
    destinoregioes = df_filtro_regioes['Destino_Regiões'].values[0]
    estadodestino = df_filtro_regioes['UF'].values[0]
    origemlocal = df_filtro_carga['Origem_Local'].values[0]
    tipo = df_filtro_carga['Tipo'].values[0]
    valorfretekg = fretepeso /peso_digitado
    st.divider()
    
    if fretepeso == 0:
      st.error("Não temos valor para a **FAIXA de PESO** escolhida, por favor escolha outra!")
    else:
      st.success("𝖢𝗈𝗇𝗌𝖾𝗀𝗎𝗂𝗆𝗈𝗌 𝖼𝖺𝗅𝖼𝗎𝗅𝖺𝗋 𝖺 𝗌𝗎𝖺 𝗌𝗈𝗅𝗂𝖼𝗂𝗍𝖺𝖼̧𝖺̃𝗈 𝗌𝗈𝖻𝗋𝖾 𝗈 𝖿𝗋𝖾𝗍𝖾.")
      coluna_esquerda , coluna_meio , coluna_direita = st.columns([1, 1,1])  
                  
      coluna_meio.metric(f"**O Prazo de entrega é** ",f'{prazoentrega}')
      coluna_esquerda.metric("𝗢 𝘃𝗮𝗹𝗼𝗿 𝗱𝗼 𝗙𝗿𝗲𝘁𝗲 𝗲́",f'R$ {fretepeso:,.2f} reais')
      coluna_direita.metric("𝗢 𝘃𝗮𝗹𝗼𝗿 𝗱𝗼 **KG** do produto é",f'R$ {valorfretekg:,.2f} reais')
      
      st.divider()
        
      st.write(f"❶ O **Origem** é a **{origem_local}**.")
      st.write(f"❷ O **Região** de Destino é   **{destinoregioes}**  e o Estado é **{estadodestino}**.")
      st.write(f"❸ O **Cliente** de destino é **{cliente}**.")
      st.write(f"❹ Para calcular o **FRETE TOTAL** é necessário somar: ( **Frete + Taxa NF + ADValorem + Icms )**.")
      st.write(f"❺ O **ICMS** de transporte (_é o imposto que incide sobre o serviço de transporte de cargas, seja ele rodoviário, ferroviário, aéreo ou aquaviário_)  **RJ x RJ = 22%** , **RJ x _( SP, MG, PR, SC e RS )_ = 12%** .")
      st.write(f"❻ O Tipo da Carga é **{tipo}**.")
      st.divider()

else:
    st.button("Cᥲᥣᥴᥙᥣᥲr Frᥱtᥱ",disabled=True)
    
st.divider() 