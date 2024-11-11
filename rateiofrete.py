import streamlit as st


st.set_page_config(
                    page_title="Rateio de frete cotralti",
                    layout="wide", 
                    page_icon="cotralti_logo.png",
                    #initial_sidebar_state="collapsed" # inicia com barra de filtros fechada
)
with st.sidebar: # todos os campos que estão aqui indentado dentro do with esta dentro do Sidebar
        st.title("Calculadora de Rateio")
      
        st.header("Rateio de Peso: Definição ?")
        st.divider()
        st.write("É um **cálculo** que considera o peso de cada item em relação ao peso total de um carrinho de compras ou de uma carga.")
        st.divider()
        st.write(":red[Para evitar erro ,o sistema inicia já com o Nº 1 definido.]")
        st.divider()
        st.write("""&copy; 2024 - Luis Felipe A. David.""")
        st.write("""Todos os direitos reservados""")

st.header("Rateio de  :blue[frete] por :green[peso]! ", divider='gray')
# Função para calcular o valor proporcional do frete por peso
def calcular_rateio(pesos, valor_total_frete, peso_total):
    return [(peso / peso_total) * valor_total_frete for peso in pesos]

# Interface do Streamlit

coluna_esquerda , coluna_meio , coluna_direita, coluna_direita2 = st.columns([1, 1, 1, 1])
# Entrada do peso total e valor total do frete
peso_total = coluna_esquerda.number_input("𝐃𝐢𝐠𝐢𝐭𝐞 𝐨 𝐩𝐞𝐬𝐨 𝐭𝐨𝐭𝐚𝐥 (𝐤𝐠):", min_value=0.0, step=0.1, value=1.0)
valor_total_frete = coluna_direita.number_input("𝗗𝗶𝗴𝗶𝘁𝗲 𝗼 𝘃𝗮𝗹𝗼𝗿 𝘁𝗼𝘁𝗮𝗹 𝗱𝗼 𝗳𝗿𝗲𝘁𝗲 (𝗥$):", min_value=0.0, step=0.1,value=1.0)


st.divider()


# Campo para os pesos individuais
coluna_esquerda , coluna_meio , coluna_direita, coluna_direita2 = st.columns([1, 1, 1, 1])
st.write(":red[𝗗𝗶𝗴𝗶𝘁𝗲 𝗼 𝗽𝗲𝘀𝗼 𝗱𝗲 𝗰𝗮𝗱𝗮 𝗶𝘁𝗲𝗺 𝗽𝗮𝗿𝗮 𝗼 𝗿𝗮𝘁𝗲𝗶𝗼:]")
pesos = []
fretes = []
for i in range(1, 6):  # Exemplo para até 5 itens
    peso_item = coluna_esquerda.number_input(f"𝗣𝗲𝘀𝗼 𝗱𝗼 𝗶𝘁𝗲𝗺 {i} (ᴋɢ):",min_value=0.0, step=0.1, key=f"peso_{i}")
    pesos.append(peso_item)


  # Calcula o peso total e o valor do frete já alocados

peso_informado = sum(pesos)
frete_alocado = sum(calcular_rateio(pesos, valor_total_frete, peso_total))

# Mostra o peso e valor do frete faltante

peso_faltante = max(peso_total - peso_informado, 0)  # Mostra zero se completado
frete_faltante = max(valor_total_frete - frete_alocado, 0)  # Mostra zero se completado

coluna_direita.metric(f":red[**Peso que esta faltando:**]", f'{peso_faltante:,.2f} kg')
coluna_direita2.metric(f":red[**Valor que esta faltando:**]",f' R$ {frete_faltante:,.2f}')


# Botão para calcular o rateio final
if st.button("Cᴀʟᴄᴜʟᴀʀ Rᴀᴛᴇɪᴏ", type="primary"):
        if peso_informado == peso_total:
            valores_rateio = calcular_rateio(pesos, valor_total_frete, peso_total)
            
            st.write(":green[**Rateio concluído!**]")
            for i, valor in enumerate(valores_rateio, 1):
                st.write(f":blue[𝐕𝐚𝐥𝐨𝐫 𝐝𝐨 𝐟𝐫𝐞𝐭𝐞 𝐩𝐚𝐫𝐚 𝐨 𝐢𝐭𝐞𝐦] {i}: R$ {valor:.2f}")
            
            st.success("Peso e valor do frete completados corretamente.")
        else:
            st.error("O peso total informado para os itens não corresponde ao peso total digitado. Verifique os valores.")

