import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Painel Q-Stop Tablet - MAHLE", page_icon="🛑", layout="wide")

# ==============================================================================
# 🎨 VISUAL CORPORATIVO: FUNDO AZUL ESCURO MAHLE + BOTÃO VERMELHO + LOGO
# ==============================================================================
st.markdown("""
    <style>
    /* Fundo azul escuro da tela inteira */
    .stApp {
        background-color: #0A1D37;
        color: #FFFFFF;
    }
    
    /* Deixa todos os textos, títulos e rótulos em branco */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Botão principal (Primeiro botão) em VERMELHO FORTE com fonte BRANCA */
    .stButton > button[kind="primary"] {
        background-color: #D90429 !important;
        color: #FFFFFF !important;
        border: 2px solid #FF4D6D !important;
        font-weight: bold !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #A4001D !important;
        border-color: #FFFFFF !important;
    }

    /* Melhora o contraste dos botões secundários no fundo escuro */
    .stButton > button[kind="secondary"] {
        background-color: #16325C;
        color: #FFFFFF;
        border: 1px solid #3B6998;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #21467D;
        border-color: #FFFFFF;
    }

    /* Estilo do campo de texto do operador */
    .stTextInput > div > div > input {
        background-color: #16325C;
        color: #FFFFFF;
        border: 1px solid #3B6998;
    }

    /* Posiciona a logo da MAHLE no canto superior direito */
    .logo-mahle {
        position: fixed;
        top: 55px;
        right: 35px;
        z-index: 9999;
        background-color: #FFFFFF;
        padding: 8px 14px;
        border-radius: 6px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
    }

    /* Cartão VERDE (Linha Liberada) */
    .card-verde {
        background-color: #1B7F3A;
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 8px;
        border-left: 8px solid #2ECC71;
        font-size: 18px;
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
    }

    /* Cartão VERMELHO (Linha Bloqueada / Alerta) */
    .card-vermelho {
        background-color: #D90429;
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 8px;
        border-left: 8px solid #FF8FA3;
        font-size: 18px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.4);
        margin-bottom: 15px;
    }
    </style>

    <div class="logo-mahle">
        <img src="https://wikimedia.org" width="140">
    </div>
""", unsafe_allow_html=True)
# ==============================================================================

MOTIVOS_DE_PARADA = [
    "🛑 PARADA POR QUALIDADE (Q-Stop)",
    "🔧 FALHA MECÂNICA / MANUTENÇÃO",
    "⚡ FALHA ELÉTRICA / AUTOMAÇÃO",
    "📦 FALTA DE MATÉRIA-PRIMA / INSUMO",
    "⚙️ AJUSTE DE MÁQUINA / SETUP",
    "🦺 SEGURANÇA / ERGONOMIA",
    "🔩 FALHA NA INSERÇÃO DO TUBO",
]

if "status_linha" not in st.session_state:
    st.session_state.status_linha = "🟢 OPERANDO NORMALMENTE"
if "historico_paradas" not in st.session_state:
    st.session_state.historico_paradas = []

st.title("🖥️ Terminal de Produção - Sistema Q-Stop")
st.markdown(f"### Status Atual da Linha: **{st.session_state.status_linha}**")
st.markdown("---")

col_acoes, col_status = st.columns(2)

with col_acoes:
    st.subheader("🚨 ACIONAMENTO RÁPIDO (Toque no Motivo)")
    operador = st.text_input("Identificação do Operador (Nome ou ID):", key="op_id")
    
    st.markdown("---")
    st.write("Selecione o motivo para **PARAR A LINHA** imediatamente:")
    
    motivo_selecionado = None
    for i, motivo in enumerate(MOTIVOS_DE_PARADA):
        tipo_botao = "primary" if i == 0 else "secondary"
        if st.button(motivo, key=f"btn_{i}", use_container_width=True, type=tipo_botao):
            motivo_selecionado = motivo
    
    if motivo_selecionado:
        if not operador:
            st.error("⚠️ Erro: Insira sua identificação antes de acionar o Q-Stop!")
        else:
            st.session_state.status_linha = f"🔴 PARADA: {motivo_selecionado.upper()}"
            nova_parada = {
                "ID": len(st.session_state.historico_paradas) + 1,
                "Operador": operador,
                "Motivo": motivo_selecionado,
                "Hora Início": datetime.now().strftime("%H:%M:%S"),
                "Hora Fim": "Em andamento",
                "Status": "Aberto"
            }
            st.session_state.historico_paradas.append(nova_parada)
            st.toast("Alerta enviado para a gestão!", icon="🚨")
            st.rerun()

with col_status:
    st.subheader("📊 Situação do Turno")
    
    if len(st.session_state.historico_paradas) == 0:
        st.markdown('<div class="card-verde">✅ Linha liberada e operando sem pendências neste turno.</div>', unsafe_allow_html=True)
    else:
        df = pd.DataFrame(st.session_state.historico_paradas)
        paradas_abertas = df[df["Status"] == "Aberto"]
        
        if not paradas_abertas.empty:
            atual = paradas_abertas.iloc[-1]
            st.markdown(f"""
                <div class="card-vermelho">
                    <div style="font-size: 22px; font-weight: bold; margin-bottom: 8px;">⚠️ LINHA BLOQUEADA</div>
                    <div><strong>Motivo:</strong> {atual['Motivo']}</div>
                    <div><strong>Início:</strong> {atual['Hora Início']} por <strong>{atual['Operador']}</strong></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("✅ RESOLVIDO - RETOMAR PRODUÇÃO", use_container_width=True, type="secondary"):
                idx_atual = df[df["Status"] == "Aberto"].index[-1]
                st.session_state.historico_paradas[idx_atual]["Status"] = "Resolvido"
                st.session_state.historico_paradas[idx_atual]["Hora Fim"] = datetime.now().strftime("%H:%M:%S")
                st.session_state.status_linha = "🟢 OPERANDO NORMALMENTE"
                st.rerun()
        else:
            st.markdown('<div class="card-verde">✅ Linha liberada e operando sem pendências.</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        st.write("**Últimas ocorrências do tablet:**")
        st.dataframe(df[["Motivo", "Hora Início", "Hora Fim", "Status"]].tail(5), use_container_width=True, hide_index=True)
