import json
from uuid import uuid4

from agente import criar_agente, perguntar


def validar(agente, sessao, pergunta, ferramentas, termos=()):
    resposta, acoes = perguntar(agente, pergunta, sessao)
    print("\nPergunta:", pergunta)
    print("Ferramentas:", [a["nome"] for a in acoes])
    print("Resposta:", resposta)
    nomes = {a["nome"] for a in acoes}
    assert set(ferramentas) <= nomes, "Ferramenta esperada não utilizada"
    for nome in ferramentas:
        resultados = [json.loads(a["resultado"]) for a in acoes if a["nome"] == nome]
        assert any(r.get("livros") or r.get("resultados") for r in resultados), nome
    for termo in termos:
        assert termo.lower() in resposta.lower(), "Termo esperado: " + termo
    assert resposta.strip()
    print("Resultado: PASSOU")


if __name__ == "__main__":
    agente = criar_agente()
    sessao = str(uuid4())
    validar(agente, sessao, "Encontre três livros sobre Python usando a busca de livros.",
            ["buscar_livros"], ["Python"])
    validar(agente, sessao, "Quem escreveu o livro 1984 (Nineteen Eighty-Four)? Pesquise o livro e a biografia de seu autor.",
            ["buscar_livros", "pesquisar_autor"], ["Orwell"])
    validar(agente, sessao, "Encontre outro livro do autor que você acabou de pesquisar. Informe também o nome dele.",
            ["buscar_livros"], ["Orwell"])
