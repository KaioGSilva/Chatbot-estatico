import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from PIL import Image

# 1. Configuração Inicial
st.set_page_config(page_title="Consultório Dra. Marta Rodrigues", page_icon="💜", layout="centered")

st.markdown("""
    <style>
    /* Estiliza o fundo da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Estiliza os cartões de métricas (Indicadores) */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #eeeeee;
    }
    
    /* Melhora o visual dos botões na sidebar */
    .stButton>button {
        border-radius: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE APOIO ---
def salvar_dados(dados):
    arquivo = "relatorio_agendamentos.csv"
    df = pd.DataFrame([dados])
    if not os.path.exists(arquivo):
        df.to_csv(arquivo, index=False, sep=';', encoding='utf-8-sig')
    else:
        df.to_csv(arquivo, mode='a', index=False, header=False, sep=';', encoding='utf-8-sig')

def verificar_disponibilidade(data, hora):
    arquivo = "relatorio_agendamentos.csv"
    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo, sep=';', encoding='utf-8-sig')
        conflito = df[(df['Data'] == data) & (df['Horário'] == hora)]
        return not conflito.empty
    return False

# ... (mantenha os seus imports e funções de salvar/conflito no topo)

# --- DICIONÁRIO DE PREÇOS (Para Gestão de Faturamento) ---
tabela_precos = {
    "Consultas pediátricas": 250.00,
    "Atendimento para recém-nascidos": 300.00,
    "Vacinação": 150.00,
    "Acompanhamento do crescimento infantil": 200.00,
    "Orientação nutricional": 180.00,
    "Atendimento de urgências leves": 350.00,
    "Exames e check-up": 220.00,
    "Agendamento online": 0.00  # Taxa de agendamento se houver
}

# --- BARRA LATERAL (SIDEBAR) EVOLUÍDA ---
with st.sidebar:
    st.header("🏥 Gestão Dra. Marta")
    
    # Botão de WhatsApp (Ideia 4)
    st.link_button("💬 Falar com a Recepção", "https://wa.me/551198873061551999999999?text=Olá, gostaria de informações sobre os agendamentos.")
    
    st.divider()

    if os.path.exists("relatorio_agendamentos.csv"):
        df_gestao = pd.read_csv("relatorio_agendamentos.csv", sep=';', encoding='utf-8-sig')
        
        # CÁLCULO DE FATURAMENTO (Ideia 3)
        # Criamos uma nova coluna de valor baseada no serviço escolhido
        df_gestao['Valor'] = df_gestao['Serviço'].map(tabela_precos)
        faturamento_total = df_gestao['Valor'].sum()
        
        st.subheader("📈 Indicadores de Desempenho")
        col_met1, col_met2 = st.columns(2)
        col_met1.metric("Total Consultas", len(df_gestao))
        col_met2.metric("Faturamento Prev.", f"R$ {faturamento_total:,.2f}")
        
        # Pequeno gráfico de pizza para ver a distribuição de serviços
        import plotly.express as px
        fig = px.pie(df_gestao, names='Serviço', title='Distribuição de Serviços', hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        st.write("📋 Lista de Pacientes:")
        st.dataframe(df_gestao[['Criança', 'Data', 'Serviço']])
    else:
        st.info("Os indicadores aparecerão após o primeiro agendamento.")

# ... (Mantenha o resto do código do chat e formulário abaixo)

# --- CABEÇALHO ---
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image(Image.open("logo.png"), width=100)
    except: pass
with col2:
    st.title("Assistente Virtual")
    st.write("Dra. Marta Rodrigues - Pediatria")

st.divider()

# --- MEMÓRIA DO CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Escolha uma opção:\n\n"
                                        "1️⃣ **Quem somos**\n"
                                        "2️⃣ **Agendar consulta**\n"
                                        "3️⃣ **Horário de funcionamento**\n"
                                        "4️⃣ **Nossos Serviços**\n"
                                        "5️⃣ **Endereço e Mapa**\n"
                                        "6️⃣ **Meus Agendamentos**\n"
                                        "7️⃣ **Valores dos Serviços**"}
    ]

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- PROCESSAMENTO DE ENTRADA (ÚNICO INPUT) ---
if prompt := st.chat_input("Como posso ajudar?"):
    # Adiciona a fala do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    resposta = ""
    
    if prompt == "1":
        resposta = "🏠 **Quem Somos:** Dra. Marta Rodrigues é especialista em pediatria humanizada, focada no desenvolvimento saudável de crianças e recém-nascidos."
    
    elif prompt == "3":
        resposta = "🕒 **Horário de Funcionamento:**\n- Segunda a Sexta: 08:00 às 18:00\n- Sábados: 08:00 às 12:00"
    
    elif prompt == "4":
        resposta = """🩺 **Nossos Serviços detalhados:**
        
* **Consultas pediátricas:** Consultas de rotina para acompanhar a saúde, prevenir doenças e orientar os responsáveis.
* **Atendimento para recém-nascidos:** Acompanhamento especializado nos primeiros dias de vida (amamentação, sono e higiene).
* **Vacinação:** Aplicação de vacinas conforme o calendário infantil oficial.
* **Acompanhamento do crescimento:** Monitoramento de peso, altura e desenvolvimento físico/cognitivo.
* **Orientação nutricional:** Auxílio na introdução alimentar e hábitos saudáveis.
* **Atendimento de urgências leves:** Casos como febre, gripe, tosse, alergias e sintomas comuns.
* **Exames e check-up:** Avaliações preventivas para acompanhar a saúde geral da criança.
* **Agendamento online:** Praticidade no agendamento de serviços de forma rápida e segura."""

    elif prompt == "5":
        resposta = "📍 **Endereço:** Av. Itaquaquecetuba, 711 - Vila Monte Belo, Itaquaquecetuba - SP.\n\n[Clique aqui para abrir o Google Maps](https://www.google.com/maps/search/?api=1&query=Av.+Itaquaquecetuba,+711+-+Vila+Monte+Belo,+Itaquaquecetuba+-+SP)"

    elif prompt == "6":
        resposta = "🔍 Por favor, use a barra lateral para consultar seus agendamentos ou digite o nome do responsável aqui."

    elif prompt == "7":
        # Criamos uma tabela visual para os valores
        resposta = "💰 **Tabela de Valores - Consultório Dra. Marta Rodrigues**\n\n"
        resposta += "| Serviço | Valor |\n"
        resposta += "| :--- | :--- |\n"
        for servico, valor in tabela_precos.items():
            if valor > 0:
                resposta += f"| {servico} | R$ {valor:.2f} |\n"
            else:
                resposta += f"| {servico} | Gratuito/Sob consulta |\n"
        
        resposta += "\n*Valores sujeitos a alteração. Aceitamos cartões de crédito, débito e PIX.*"

    elif prompt == "2":
        st.session_state.agendando = True
        resposta = "📅 Excelente! Preencha o formulário abaixo para confirmar seu horário:"

    if resposta:
        st.session_state.messages.append({"role": "assistant", "content": resposta})
    
    st.rerun() # Limpa a tela e evita duplicação de inputs

# --- FORMULÁRIO DE AGENDAMENTO (SÓ APARECE SE OPT 2 FOR ESCOLHIDA) ---
if st.session_state.get("agendando"):
    with st.chat_message("assistant"):
        with st.form("form_chat"):
            resp = st.text_input("Nome do Responsável")
            crianca = st.text_input("Nome da Criança")
            data_sel = st.date_input("Data da Consulta", min_value=date.today())
            hora_sel = st.selectbox("Horário", ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"])
            serv_sel = st.selectbox("Selecione o Serviço", [
                "Consultas pediátricas",
                "Atendimento para recém-nascidos",
                "Vacinação",
                "Acompanhamento do crescimento infantil",
                "Orientação nutricional",
                "Atendimento de urgências leves",
                "Exames e check-up",
                "Agendamento online"
            ])
            
            if st.form_submit_button("Confirmar Agendamento"):
                data_f = data_sel.strftime('%d/%m/%Y')
                
                # --- NOVAS VALIDAÇÕES DE SEGURANÇA ---
                
                # 1. Bloqueia Domingos (weekday 6)
                if data_sel.weekday() == 6:
                    st.error("❌ O consultório não realiza atendimentos aos domingos. Por favor, escolha de segunda a sábado.")
                
                # 2. Bloqueia Sábados após as 12h (weekday 5)
                elif data_sel.weekday() == 5 and int(hora_sel[:2]) >= 12:
                    st.error("❌ Aos sábados, o consultório atende apenas até as 12:00. Por favor, escolha um horário na parte da manhã.")
                
                # 3. Verifica se o horário já está ocupado no CSV
                elif verificar_disponibilidade(data_f, hora_sel):
                    st.error("❌ Desculpe, este horário já está ocupado! Tente outro.")
                
                # 4. Se passar em tudo, salva o agendamento
                elif resp and crianca:
                    dados = {
                        "Responsável": resp, 
                        "Criança": crianca, 
                        "Data": data_f, 
                        "Horário": hora_sel, 
                        "Serviço": serv_sel, 
                        "Registro": datetime.now().strftime('%d/%m/%Y %H:%M')
                    }
                    salvar_dados(dados)
                    st.success("✅ Agendamento realizado com sucesso!")
                    st.session_state.messages.append({"role": "assistant", "content": f"✅ Confirmado: {serv_sel} para {crianca} em {data_f} às {hora_sel}."})
                    st.session_state.agendando = False
                    st.rerun()
                else:
                    st.warning("⚠️ Por favor, preencha o nome do responsável e da criança.")

# --- BARRA LATERAL (ADMIN E CONSULTA) ---
# --- ÁREA DO ADMINISTRADOR (SIDEBAR EVOLUÍDA) ---
# --- ÁREA DE GESTÃO (SIDEBAR) ---
with st.sidebar:
   
    st.divider()

    if os.path.exists("relatorio_agendamentos.csv"):
        df_gestao = pd.read_csv("relatorio_agendamentos.csv", sep=';', encoding='utf-8-sig')
        df_gestao['Valor'] = df_gestao['Serviço'].map(tabela_precos)

        # 2. SEÇÃO: INDICADORES (KPIs)
        st.markdown("#### 📈 Indicadores de Desempenho")
        m1, m2 = st.columns(2)
        m1.metric("Agendados", len(df_gestao))
        # Calcula faturamento de forma limpa
        faturamento = df_gestao['Valor'].sum()
        m2.metric("Receita", f"R$ {faturamento:,.0f}")

        st.divider()

        # 3. SEÇÃO: RESUMO FINANCEIRO E DISTRIBUIÇÃO
        # Usamos um Expander para economizar espaço e parecer mais sofisticado
        with st.expander("💰 Detalhamento Financeiro", expanded=False):
            st.write("**Faturamento por Categoria:**")
            receita_por_servico = df_gestao.groupby('Serviço')['Valor'].sum().reset_index()
            st.dataframe(receita_por_servico, hide_index=True, use_container_width=True)
            
            # Gráfico de Rosca (Donut Chart) - Mais moderno que pizza
            fig = px.pie(df_gestao, names='Serviço', hole=0.6, 
                         color_discrete_sequence=px.colors.qualitative.Prism)
            fig.update_layout(showlegend=False, height=150, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # 4. SEÇÃO: LISTA DE AGENDAMENTOS (TABELA PRO)
        st.markdown("#### 📅 Próximos Atendimentos")
        # Filtramos para mostrar os 5 mais recentes de forma organizada
        df_recente = df_gestao[['Data', 'Horário', 'Criança']].tail(5)
        st.table(df_recente) # Tabela estática é mais "limpa" para listas curtas

        # BOTÃO DE EXPORTAÇÃO NO RODAPÉ
        csv = df_gestao.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button("📥 Exportar Base de Dados", csv, "gestao.csv", "text/csv", use_container_width=True)

    else:
        st.info("Sem dados para exibir no momento.")

