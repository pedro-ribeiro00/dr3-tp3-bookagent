from uuid import uuid4

import streamlit as st

from agente import criar_agente, perguntar

st.set_page_config(page_title="BookAgent", page_icon="📚")
st.title("BookAgent")
st.caption("Pesquise livros e autores com um agente de IA.")

if "agente" not in st.session_state:
    try:
        st.session_state.agente = criar_agente()
        st.session_state.sessao = str(uuid4())
        st.session_state.historico = []
    except ValueError as erro:
        st.error(str(erro))
        st.stop()

if st.sidebar.button("Nova conversa"):
    st.session_state.sessao = str(uuid4())
    st.session_state.historico = []
    st.rerun()

for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

if pergunta := st.chat_input("Digite sua pergunta sobre livros ou autores"):
    st.session_state.historico.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)
    with st.chat_message("assistant"):
        with st.spinner("Pesquisando..."):
            try:
                resposta, acoes = perguntar(
                    st.session_state.agente, pergunta, st.session_state.sessao
                )
            except Exception:
                resposta = "Não foi possível completar a consulta. Verifique a conexão e a chave da API."
                acoes = []
        st.markdown(resposta)
        if acoes:
            with st.expander("Ferramentas utilizadas"):
                for acao in acoes:
                    st.write(acao["nome"])
    st.session_state.historico.append({"role": "assistant", "content": resposta})
