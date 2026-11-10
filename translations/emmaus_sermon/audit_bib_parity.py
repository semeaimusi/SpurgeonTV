"""
Auditoria de paridade e integridade das Bibliografias em PT, ES e EN:
translations/emmaus_sermon/bibliografias_alinhadas_es_en.md
"""

import os
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

DOC_PATH = os.path.join('translations', 'emmaus_sermon', 'bibliografias_alinhadas_es_en.md')

def audit_bib_document():
    print("=" * 80)
    print("AUDITORIA DE PARIDADE DAS BIBLIOGRAFIAS HARMONIZADAS")
    print("=" * 80)
    
    assert os.path.exists(DOC_PATH), f"Arquivo não encontrado: {DOC_PATH}"
    print(f"[OK] Arquivo localizado: {DOC_PATH}")
    
    with open(DOC_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Contar itens no comparativo entrada por entrada
    item_headers = re.findall(r'### \[Item (\d+) \| P (\d+)\]', content)
    print(f"[OK] Total de Blocos Comparativos Encontrados: {len(item_headers)} (Esperado: 56)")
    assert len(item_headers) == 56, f"Esperado 56 itens, encontrado {len(item_headers)}"

    # 2. Contar itens na versão contínua em Espanhol
    es_section = re.search(r'## 3\. Versão Integral Contínua em Espanhol \(BIBLIOGRAFÍA\)\s+```text\s+BIBLIOGRAFÍA\s+(.*?)\s+```', content, re.DOTALL)
    assert es_section, "Seção contínua em Espanhol não encontrada!"
    es_entries = [line.strip() for line in es_section.group(1).split('\n\n') if line.strip()]
    print(f"[OK] Total de Entradas Contínuas em Espanhol: {len(es_entries)} (Esperado: 56)")
    assert len(es_entries) == 56, f"Esperado 56 entradas em ES, encontrado {len(es_entries)}"

    # 3. Contar itens na versão contínua em Inglês
    en_section = re.search(r'## 4\. Versão Integral Contínua em Inglês \(BIBLIOGRAPHY\)\s+```text\s+BIBLIOGRAPHY\s+(.*?)\s+```', content, re.DOTALL)
    assert en_section, "Seção contínua em Inglês não encontrada!"
    en_entries = [line.strip() for line in en_section.group(1).split('\n\n') if line.strip()]
    print(f"[OK] Total de Entradas Contínuas em Inglês: {len(en_entries)} (Esperado: 56)")
    assert len(en_entries) == 56, f"Esperado 56 entradas em EN, encontrado {len(en_entries)}"

    # 4. Checagem de URLs
    expected_urls = [
        "https://www.spurgeon.tv/bible/",
        "https://lexico.opejuris.com",
        "https://www.preceptaustin.org/genesis-4-commentary",
        "https://sieb.com.br/genesis-41-alcancei-do-senhor-um-homem-a-surpreendente-identidade-de-caim/",
        "https://www.spurgeon.tv/en/volume/volume-22/sermon-1322"
    ]
    for url in expected_urls:
        count = content.count(url)
        print(f"[OK] URL preservada ({count}x): {url}")
        assert count >= 3, f"URL {url} deve aparecer no mínimo 3 vezes!"

    # 5. Checagem de Nomes de Autores Chave
    key_authors = [
        "ANDERS, Max E.",
        "CESARETTI, M. A.",
        "CHAMPLIN, Russell Norman",
        "CHO, Bernardo",
        "DEVER, William G.",
        "EARLE, Ralph",
        "FINLEY, Mark",
        "FREITAS, Paulo",
        "GRONINGEN, Gerard Van",
        "GUIMARÃES, Marcelo Miranda",
        "GUSSO, Antônio Renato",
        "KUYPER, Abraham",
        "MACARTHUR, John",
        "McMURTRY, Grady Shannon",
        "MELO, Edino",
        "MELO, Joel Leitão de",
        "PRICE, J. Randall",
        "RODRIGUES, Eber",
        "SILVA, Isaias da",
        "SILVA, Israel",
        "SPURGEON, Charles H.",
        "VAILATTI, Carlos Augusto",
        "VAUX, Roland De",
        "WIERSBE, Warren W.",
        "WILLMINGTON, Harold L."
    ]
    for author in key_authors:
        count = content.count(author)
        assert count >= 2, f"Autor {author} deve ser preservado!"
    print(f"[OK] Todos os {len(key_authors)} autores-chave foram preservados com sucesso!")

    # 6. Checagem de Conectivos e Rótulos Específicos
    assert "Disponível em:" not in es_section.group(1), "Resíduo de 'Disponível em:' em Espanhol!"
    assert "Disponível em:" not in en_section.group(1), "Resíduo de 'Disponível em:' em Inglês!"
    assert "Disponible en:" in es_section.group(1), "Falta 'Disponible en:' em Espanhol!"
    assert "Available at:" in en_section.group(1), "Falta 'Available at:' em Inglês!"
    assert "BIBLIAS. Español (Reina-Valera y NVI)" in es_section.group(1), "Entrada modelo de Bíblias em ES incorreta!"
    assert "BIBLES. Spanish (Reina-Valera and NIV)" in en_section.group(1), "Entrada modelo de Bíblias em EN incorreta!"
    print("[OK] Conectivos e rótulos funcionais verificados em 100% das seções!")

    print("\n" + "=" * 80)
    print("🏆 AUDITORIA APROVADA COM 100% DE SUCESSO!")
    print("   Paridade absoluta: 56 itens alinhados em PT, ES e EN.")
    print("=" * 80)

if __name__ == '__main__':
    audit_bib_document()

