import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Conexão com Google Sheets
def get_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Nome_Da_Sua_Planilha").sheet1 # Coloque o nome correto da sua planilha aqui
    return sheet

sheet = get_data()

st.title("🛡️ Painel de Controle: Drogaria União Farma")

# Lê os dados da planilha
df = pd.DataFrame(sheet.get_all_records())
config = df.iloc[0] # Pega a primeira linha da planilha

# Interface Visual
status = st.selectbox("Status do Robô", ["LIGADO", "DESLIGADO"], index=0 if config['Status'] == 'LIGADO' else 1)
prompt = st.text_area("Prompt do Sistema (Instruções da IA)", config['Prompt_Sistema'])
horario = st.text_input("Horário de Atendimento", config['Horario_Inicio'])

if st.button("Salvar Alterações"):
    # Atualiza a planilha
    sheet.update_cell(2, 1, status)    # Atualiza coluna 1 (Status)
    sheet.update_cell(2, 2, prompt)    # Atualiza coluna 2 (Prompt)
    sheet.update_cell(2, 3, horario)   # Atualiza coluna 3 (Horário)
    st.success("Configurações salvas na planilha!")