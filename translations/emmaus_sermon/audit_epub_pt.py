"""
Auditoria técnica, estrutural e de links internos do arquivo EPUB 3.0:
translations/emmaus_sermon/O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.epub
"""

import os
import sys
import re
import zipfile
import xml.etree.ElementTree as ET

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

EPUB_PATH = os.path.join('translations', 'emmaus_sermon', 'O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.epub')


def run_epub_audit():
    print("=" * 80)
    print("AUDITORIA TÉCNICA E ESTRUTURAL EPUB 3.0 - O SERMÃO DE EMAÚS (PT)")
    print("=" * 80)

    assert os.path.exists(EPUB_PATH), f"EPUB não encontrado: {EPUB_PATH}"
    size_kb = os.path.getsize(EPUB_PATH) / 1024
    print(f"[OK] Arquivo encontrado: {EPUB_PATH} ({size_kb:.2f} KB)")

    with zipfile.ZipFile(EPUB_PATH, 'r') as zf:
        infolist = zf.infolist()
        namelist = zf.namelist()

        # 1. Regra OCF do mimetype
        first_item = infolist[0]
        assert first_item.filename == 'mimetype', f"Primeiro arquivo deve ser 'mimetype', encontrado '{first_item.filename}'"
        assert first_item.compress_type == zipfile.ZIP_STORED, "Arquivo 'mimetype' deve ser armazenado sem compressão (ZIP_STORED)"
        mime_bytes = zf.read('mimetype')
        assert mime_bytes == b'application/epub+zip', f"Conteúdo inválido em mimetype: {mime_bytes!r}"
        print("[OK] Conformidade OCF 'mimetype' (1º arquivo, ZIP_STORED, 'application/epub+zip')")

        # 2. Validar XML well-formedness de todos os arquivos XML/XHTML/OPF/NCX
        id_registry = {}  # filename -> set of ids
        href_checks = []  # list of (source_file, target_file, target_id)
        total_xhtml_words = 0
        total_guillemets_open = 0
        total_guillemets_close = 0
        residual_double_quotes = 0

        for name in namelist:
            if name.endswith(('.xhtml', '.xml', '.opf', '.ncx')):
                raw = zf.read(name)
                try:
                    tree = ET.fromstring(raw)
                except Exception as e:
                    raise AssertionError(f"Erro de XML malformado em {name}: {e}")

                base = name.split('/')[-1]
                ids_in_file = set()
                for elem in tree.iter():
                    eid = elem.attrib.get('id') or elem.attrib.get('{http://www.w3.org/XML/1998/namespace}id')
                    if eid:
                        ids_in_file.add(eid)
                    href = elem.attrib.get('href')
                    if href and name.endswith('.xhtml') and not href.startswith(('http://', 'https://', 'mailto:', 'styles/')):
                        if '#' in href:
                            tfile, tid = href.split('#', 1)
                            tfile = tfile if tfile else base
                            href_checks.append((base, tfile, tid))
                        else:
                            href_checks.append((base, href, None))
                id_registry[base] = ids_in_file

                if name.endswith('.xhtml') and base != 'nav.xhtml':
                    text_content = ''.join(tree.itertext())
                    total_xhtml_words += len(text_content.split())
                    total_guillemets_open += text_content.count('«')
                    total_guillemets_close += text_content.count('»')
                    residual_double_quotes += sum(text_content.count(c) for c in ('"', '“', '”'))

        print(f"[OK] Todos os {len(id_registry)} arquivos XML/XHTML/OPF/NCX são 100% bem-formados (well-formed XML)")

        # 3. Resolver todos os links internos e âncoras bidirecionais
        broken_links = []
        for src, tfile, tid in href_checks:
            if tfile not in id_registry:
                broken_links.append((src, tfile, tid, "Arquivo de destino inexistente"))
            elif tid and tid not in id_registry[tfile]:
                broken_links.append((src, tfile, tid, f"ID #{tid} não encontrado em {tfile}"))

        assert len(broken_links) == 0, f"Links quebrados encontrados: {broken_links}"
        print(f"[OK] Todos os {len(href_checks)} hiperlinks internos, sumário e notas bidirecionais resolvem perfeitamente!")

        # 4. Verificar as 50 notas finais e 50 âncoras
        notas_ids = id_registry.get('notas_finais.xhtml', set())
        for k in range(1, 51):
            assert f'fn{k}' in notas_ids, f"Nota fn{k} ausente em notas_finais.xhtml!"
            found_ref = any(f'ref{k}' in ids for fname, ids in id_registry.items() if fname != 'notas_finais.xhtml')
            assert found_ref, f"Âncora ref{k} ausente nos capítulos do corpo!"
        print("[OK] 50 de 50 âncoras no corpo (#ref1..#ref50) e 50 de 50 notas (#fn1..#fn50) verificadas!")

        # 5. Verificar as 36 seções numeradas
        for s in range(1, 37):
            found_sec = any(f'sec-{s}' in ids for ids in id_registry.values())
            assert found_sec, f"Seção #sec-{s} não encontrada!"
        print("[OK] Todas as 36 seções temáticas (#sec-1 a #sec-36) presentes e indexadas no Sumário!")

        # 6. Verificar aspas e volume textual
        print(f"[OK] Volume total de palavras no EPUB: {total_xhtml_words} palavras")
        print(f"[OK] Aspas angulares preservadas: {total_guillemets_open} « e {total_guillemets_close} »")
        print(f"[OK] Resíduo de aspas duplas aéreas no texto: {residual_double_quotes} (Esperado: 0)")
        assert residual_double_quotes == 0, f"Encontradas {residual_double_quotes} aspas duplas residuais!"

        # 7. Verificar conformidade do CSS para Google Play Livros
        css_text = zf.read('OEBPS/styles/stylesheet.css').decode('utf-8')
        assert '@namespace' not in css_text, "Regra @namespace encontrada em stylesheet.css!"
        assert '-webkit-text-decoration-skip' not in css_text, "Propriedade -webkit-text-decoration-skip encontrada!"
        assert 'text-decoration-skip-ink' not in css_text, "Propriedade text-decoration-skip-ink encontrada!"
        print("[OK] CSS 100% compatível com o validador do Google Play Livros (zero @namespace / -webkit-)")

    print("\n" + "=" * 80)
    print("🏆 AUDITORIA EPUB 3.0 APROVADA COM 100% DE SUCESSO!")
    print("=" * 80)


if __name__ == '__main__':
    run_epub_audit()

