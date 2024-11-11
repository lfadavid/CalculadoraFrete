import streamlit as st
import pandas as pd

pg = st.navigation(
            {
            "Consultas na Tabela Spice ": [st.Page("calculadorafrete.py", title="Calculadora de Frete Tonelada"),
                        st.Page("fretededicado.py", title="Cálculo de Frete Dedicado"),
                        st.Page("consultarotas.py", title="Consulta por Rotas"),
                        st.Page("rateiofrete.py", title="Rateio de Frete por peso")]
            #"Conta": [st.Page(logout, title="Sair"), st.Page("criar_conta.py", title="Criar Conta")]
            }
)
pg.run()