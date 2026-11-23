import json
import unittest
from unittest.mock import Mock, patch

import requests

from ferramentas import buscar_livros, pesquisar_autor


class TestFerramentas(unittest.TestCase):
    @patch("ferramentas.requests.get")
    def test_livros(self, get):
        get.return_value = Mock()
        get.return_value.json.return_value = {"docs": [
            {"key": "/works/OL1W", "title": "1984",
             "author_name": ["George Orwell"], "first_publish_year": 1949}
        ]}
        resultado = json.loads(buscar_livros("1984"))
        self.assertEqual(resultado["livros"][0]["autores"], ["George Orwell"])
        self.assertEqual(resultado["livros"][0]["ano"], 1949)

    @patch("ferramentas.requests.get")
    def test_autor(self, get):
        get.return_value.json.return_value = {"query": {"pages": [
            {"title": "George Orwell", "extract": "Escritor britânico",
             "fullurl": "https://en.wikipedia.org/wiki/George_Orwell"}
        ]}}
        resultado = json.loads(pesquisar_autor("George Orwell"))
        self.assertEqual(resultado["resultados"][0]["titulo"], "George Orwell")

    @patch("ferramentas.requests.get")
    def test_sem_resultado(self, get):
        get.return_value.json.return_value = {"docs": []}
        self.assertEqual(json.loads(buscar_livros("inexistente")), {"livros": []})

    @patch("ferramentas.requests.get", side_effect=requests.Timeout)
    def test_falha_externa(self, get):
        self.assertIn("erro", json.loads(buscar_livros("1984")))
        self.assertIn("erro", json.loads(pesquisar_autor("Orwell")))


if __name__ == "__main__":
    unittest.main()
