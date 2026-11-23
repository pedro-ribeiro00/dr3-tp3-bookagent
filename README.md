# BookAgent — DR3 TP3

Assistente de pesquisa de livros e autores desenvolvido com Python, LangChain e Gemini.

## Problema e objetivo

Pesquisar livros e informações sobre seus autores normalmente exige abrir diferentes sites, repetir consultas e reunir os dados manualmente. O BookAgent foi pensado para estudantes, professores e leitores que querem realizar essas consultas em uma conversa.

Funcionalidades: buscar livros, consultar biografias, apresentar fontes e responder perguntas relacionadas ao histórico da sessão.

## Como funciona

O agente usa Gemini 3.5 Flash-Lite por padrão e duas ferramentas externas:
- `buscar_livros`: consulta a Open Library e retorna título, autores, ano e link.
- `pesquisar_autor`: consulta a Wikipédia e retorna título, resumo e link.

O `create_agent` do LangChain implementa o ciclo ReAct: o modelo decide uma ação, executa a ferramenta, recebe a observação e pode fazer outra chamada ou responder. A memória usa `InMemorySaver` e um identificador de conversa por sessão. O histórico é temporário.

## Execução

Requisitos: Python 3.11 ou 3.12, internet e chave Gemini ([Google AI Studio](https://aistudio.google.com/api-keys)).

    python -m venv .venv

Ative o ambiente no Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`. No macOS/Linux: `source .venv/bin/activate`.

    python -m pip install -r requirements.txt

Copie `.env.example` para `.env` e preencha `GOOGLE_API_KEY` com sua chave. O modelo pode ser alterado em `GEMINI_MODEL`. Nunca publique o arquivo .env.

    python -m streamlit run app.py

## Casos de uso e testes

| Caso | Pergunta ou situação | Resultado esperado |
| --- | --- | --- |
| Busca | Encontrar três livros sobre Python | Retornar livros da Open Library |
| ReAct | Identificar o autor de 1984 e consultar sua biografia | Usar as duas ferramentas e informar George Orwell |
| Memória | Encontrar outro livro do autor anterior | Recuperar o autor da conversa e consultar livros |
| Erros | Consulta sem resultado ou timeout | Informar ausência de dados ou erro |

Testes unitários (respostas simuladas): `python -m unittest -v testes`.

Teste de integração (Gemini e APIs reais): `python teste_integracao.py`.

### Resultados observados

A execução nº 1 do workflow [Testes BookAgent](https://github.com/pedro-ribeiro00/dr3-tp3-bookagent/actions) (commit `86f6c2c`) foi concluída com sucesso em 56 segundos, conforme o status do GitHub Actions.

- Busca de livros: passou na validação de uso da ferramenta, retorno de dados e presença do termo Python na resposta.
- ReAct: passou na validação de chamadas às duas ferramentas, retorno de dados e identificação de Orwell na resposta.
- Memória: passou na consulta seguinte, na mesma sessão, utilizando o autor da pergunta anterior.
- Erros e ausência de resultados: os quatro testes unitários passaram com respostas simuladas, incluindo timeout das APIs.

O workflow também verificou a compilação dos módulos Python. A execução de integração exige chave válida e cota de API. Os testes verificam o comportamento do agente; a interface Streamlit não foi avaliada visualmente pelo workflow.

## Comparação com a abordagem manual

Sem o agente, o usuário precisaria consultar a Open Library, identificar o autor, pesquisar sua biografia e repetir o contexto a cada nova pesquisa. O agente reúne essas etapas e mantém o contexto durante a conversa. As fontes continuam disponíveis para conferência e as respostas dependem da qualidade das APIs e do modelo.

## Referências

- [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [Open Library API](https://openlibrary.org/developers/api)
- [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page)
- [Gemini API](https://ai.google.dev/gemini-api/docs)
