import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st


# ==========================================
# 1. CONEXÃO COM O GOOGLE SHEETS VIA SECRETS
# ==========================================
def conectar_planilha():
  # Busca as credenciais de segurança guardadas no "Secrets" do Streamlit
  creds_dict = dict(st.secrets["gcp"])

  scope = [
      "https://spreadsheets.google.com/feeds",
      "https://www.googleapis.com/auth/drive",
  ]
  creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

  client = gspread.authorize(creds)

  # ATENÇÃO: Substitua aqui pelo nome EXATO da sua planilha lá no Google Drive
  sheet = client.open("Nome_Da_Sua_Planilha").sheet1
  return sheet


# ==========================================
# 2. INTERFACE DO PAINEL (STREAMLIT)
# ==========================================
st.set_page_config(page_title="Painel do Robô", page_icon="💊")
st.title("🛡️ Painel de Controle: Drogaria União Farma")
st.write("Altere as regras e promoções do atendimento sem mexer no código.")

try:
  # Conecta na planilha e lê os dados atuais
  sheet = conectar_planilha()
  df = pd.DataFrame(sheet.get_all_records())

  # Pega a primeira linha de dados da planilha
  config_atual = df.iloc[0]

  # ==========================================
  # 3. CAMPOS DE EDIÇÃO NA TELA
  # ==========================================
  status_atual = config_atual["Status"]
  index_status = 0 if status_atual == "LIGADO" else 1

  status = st.selectbox(
      "Status do Robô (Liga/Desliga)", ["LIGADO", "DESLIGADO"], index=index_status
  )

  prompt = st.text_area(
      "Instruções do Bot (Prompt do Sistema)",
      value=config_atual["Prompt_Sistema"],
      height=200,
      help=(
          "Escreva aqui como o robô deve responder, quais são as promoções do"
          " dia, regras para entrega, etc."
      ),
  )

  col1, col2 = st.columns(2)
  with col1:
    horario_inicio = st.text_input(
        "Horário de Início", value=config_atual["Horario_Inicio"]
    )
  with col2:
    horario_fim = st.text_input(
        "Horário de Término", value=config_atual.get("Horario_Fim", "18:00")
    )

  # ==========================================
  # 4. BOTÃO PARA SALVAR AS MUDANÇAS
  # ==========================================
  if st.button("💾 Salvar Alterações na Planilha", type="primary"):
    # Atualiza as células da primeira linha de dados (linha 2 da planilha, pois linha 1 é o cabeçalho)
    sheet.update_cell(2, 1, status)  # Coluna A (Status)
    sheet.update_cell(2, 2, prompt)  # Coluna B (Prompt_Sistema)
    sheet.update_cell(2, 3, horario_inicio)  # Coluna C (Horario_Inicio)
    sheet.update_cell(2, 4, horario_fim)  # Coluna D (Horario_Fim)

    st.success(
        "✅ Configurações salvas com sucesso! O robô já está obedecendo às"
        " novas regras."
    )

except Exception as e:
  st.error(f"Erro ao conectar ou ler a planilha: {e}")
  st.info(
      "Verifique se o nome da planilha está correto na linha 22 do código e se"
      " o e-mail da conta de serviço foi adicionado como Editor na planilha."
  )