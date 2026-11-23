import json

import requests

HEADERS = {"User-Agent": "BookAgent/1.0 (https://github.com/pedro-ribeiro00/dr3-tp3-bookagent)"}


def buscar_livros(consulta: str) -> str:
    """Busca até cinco livros na Open Library por título, assunto ou autor."""
    try:
        resposta = requests.get(
            "https://openlibrary.org/search.json",
            params={"q": consulta, "limit": 5,
                    "fields": "key,title,author_name,first_publish_year"},
            headers=HEADERS, timeout=20,
        )
        resposta.raise_for_status()
        livros = []
        for item in resposta.json().get("docs", []):
            livros.append({
                "titulo": item.get("title"),
                "autores": item.get("author_name", []),
                "ano": item.get("first_publish_year"),
                "url": "https://openlibrary.org" + item.get("key", ""),
            })
        return json.dumps({"livros": livros}, ensure_ascii=False)
    except (requests.RequestException, ValueError):
        return json.dumps({"erro": "Não foi possível consultar a Open Library."}, ensure_ascii=False)


def pesquisar_autor(nome: str) -> str:
    """Consulta a Wikipédia em inglês para obter uma breve descrição de um autor ou assunto."""
    try:
        resposta = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "query", "generator": "search", "gsrsearch": nome,
                    "gsrlimit": 1, "prop": "extracts|info", "exintro": 1,
                    "explaintext": 1, "inprop": "url", "format": "json",
                    "formatversion": 2},
            headers=HEADERS, timeout=20,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        if "error" in dados:
            return json.dumps({"erro": "A Wikipédia retornou um erro."}, ensure_ascii=False)
        paginas = dados.get("query", {}).get("pages", [])
        resultados = [
            {"titulo": p.get("title"), "resumo": p.get("extract", "")[:1800],
             "url": p.get("fullurl")}
            for p in paginas
        ]
        return json.dumps({"resultados": resultados}, ensure_ascii=False)
    except (requests.RequestException, ValueError):
        return json.dumps({"erro": "Não foi possível consultar a Wikipédia."}, ensure_ascii=False)
