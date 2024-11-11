import streamlit as st
import pandas as pd

st.set_page_config(
                    page_title="Consulta por Rotas",
                    layout="wide", 
                    page_icon="cotralti_logo.png",
                    #initial_sidebar_state="collapsed" # inicia com barra de filtros fechada
)
# Add custom CSS to hide the GitHub icon
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""

def hide_anchor_link():
    st.markdown(
        body="""
        <style>
            h1 > div > a {
                display: none;
            }
            h2 > div > a {
                display: none;
            }
            h3 > div > a {
                display: none;
            }
            h4 > div > a {
                display: none;
            }
            h5 > div > a {
                display: none;
            }
            h6 > div > a {
                display: none;
            }
        </style>
        """,
         unsafe_allow_html=True,
)

#Editar a Imagem da Cotralti e deixar ela centralizada
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width:50%;
        }
    </style>
    """, unsafe_allow_html=True
)

hide_github_icon = """
#GithubIcon {
  visibility: hidden;
   display:none;
    opacity:0;
}
"""
st.header("Consulta por :blue[Rotas] ", divider='green')

DataFrame = pd.read_excel("Base Rotas.xlsx", index_col=4)#index_col=2
DataFrame["Cidade"] = DataFrame["Cidade"].astype("string")
DataFrame["Tabela de Fat."] = DataFrame["Tabela de Fat."].astype("string")
DataFrame["Estado de Destino"]  = DataFrame["Estado de Destino"]

with open ('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header("Filtro")

cidade = st.sidebar.selectbox(
                key=1,
                label="Cidade",
                options=DataFrame["Cidade"].unique(),
                help="Selecione a Cidade e click nela",
                placeholder="Selecione a cidade",
                index=None
                
)

tabela_de_fat = st.sidebar.multiselect(
                key=2,
                label="Tabela de Fat.",
                options=DataFrame["Tabela de Fat."].unique(),
                placeholder="Selecione a Rota",
                help="Selecione a rota e click nela."
                
            )
if cidade:
    if len(cidade) != None:
        DataFrame = DataFrame.query("Cidade== @cidade")
        st.success("Encontramos a cidade selecionada!")

elif tabela_de_fat:
    if len(tabela_de_fat) != None:
        DataFrame = DataFrame.query(" `Tabela de Fat.`== @tabela_de_fat")
        st.success("Encontramos a rota selecionada!")  
       
colunas_aparecer = ["Tabela de Fat.", "Saída Spice","Cidade", "Região", "Dias de Entrega", "Lead Time"]
st.dataframe(DataFrame[colunas_aparecer],use_container_width=True,
                column_config={ "Lead Time": st.column_config.ProgressColumn("Tempo de Entrega",format="D+%d", min_value=1, max_value=5),
                               
                })
st.write("""
         &copy; 2024 - Luis Felipe A. David. Todos os direitos reservados
         """)