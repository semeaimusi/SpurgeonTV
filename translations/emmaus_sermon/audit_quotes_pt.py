"""
Auditoria exaustiva da versão em português com aspas angulares:
O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.docx
"""

import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ORIG_DOCX = os.path.join('public', 'downloads', 'O_Sermao_de_Emaus_Versao_NVI_Atualizado.docx')
NEW_DOCX = os.path.join('translations', 'emmaus_sermon', 'O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.docx')

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def run_audit():
    print("=" * 80)
    print("AUDITORIA COMPLETA: VERSÃO EM PORTUGUÊS COM ASPAS ANGULARES (« »)")
    print("=" * 80)
    
    assert os.path.exists(NEW_DOCX), f"Arquivo não encontrado: {NEW_DOCX}"
    file_size_kb = os.path.getsize(NEW_DOCX) / 1024
    print(f"[OK] Arquivo gerado com sucesso: {NEW_DOCX} ({file_size_kb:.2f} KB)")
    
    with zipfile.ZipFile(ORIG_DOCX, 'r') as z_orig, zipfile.ZipFile(NEW_DOCX, 'r') as z_new:
        # 1. AUDITAR DOCUMENT.XML
        print("\n" + "-" * 70)
        print("1. AUDITORIA DO CORPO DO LIVRO (word/document.xml)")
        print("-" * 70)
        
        orig_doc_tree = ET.fromstring(z_orig.read('word/document.xml'))
        new_doc_tree = ET.fromstring(z_new.read('word/document.xml'))
        
        orig_p = orig_doc_tree.findall('.//w:p', NS)
        new_p = new_doc_tree.findall('.//w:p', NS)
        print(f"[OK] Total de Parágrafos: {len(new_p)} (Original: {len(orig_p)})")
        assert len(new_p) == len(orig_p), "Contagem de parágrafos divergiu!"
        
        orig_anchors = orig_doc_tree.findall('.//w:endnoteReference', NS)
        new_anchors = new_doc_tree.findall('.//w:endnoteReference', NS)
        print(f"[OK] Total de Âncoras de Notas: {len(new_anchors)} (Original: {len(orig_anchors)})")
        assert len(new_anchors) == 50, f"Esperado 50 âncoras, encontrado {len(new_anchors)}"
        
        # Check quotes in prose (<w:t> elements)
        t_nodes = new_doc_tree.findall('.//w:t', NS)
        prose_text = ''.join([t.text for t in t_nodes if t.text])
        straight_d = prose_text.count('"')
        left_curly = prose_text.count('“')
        right_curly = prose_text.count('”')
        ang_left = prose_text.count('«')
        ang_right = prose_text.count('»')
        
        print(f"[OK] Resíduo de Aspas Duplas Aéreas no Texto Literário (<w:t>): {straight_d + left_curly + right_curly} (Esperado: 0)")
        assert (straight_d + left_curly + right_curly) == 0, "Ainda restam aspas duplas no corpo!"
        
        instr_nodes = new_doc_tree.findall('.//w:instrText', NS)
        instr_text = ''.join([i.text for i in instr_nodes if i.text])
        print(f"[OK] Sintaxe Técnica de Campo Word (<w:instrText>): {instr_text} (Preservada!)")
        assert 'HYPERLINK "mailto:webert@ymail.com"' in instr_text, "Campo HYPERLINK corrompido!"
        
        print(f"[OK] Aspas Angulares no Corpo: {ang_left} de abertura («) e {ang_right} de fechamento (»)")
        
        # Check spot paragraphs
        p4_text = ''.join(new_p[4].itertext())
        print(f"[OK] Amostra P 4: {p4_text}")
        assert p4_text.startswith('«E começando') and p4_text.endswith('Escrituras.»'), "P4 não formatado corretamente!"
        
        p41_text = ''.join(new_p[41].itertext())
        print(f"[OK] Amostra P 41: {p41_text}")
        assert '«adicionar»' in p41_text, "P41 não contém «adicionar»!"
        
        p55_text = ''.join(new_p[55].itertext())
        print(f"[OK] Amostra P 55: {p55_text[:120]}...")
        assert '«O que aconteceu com Jesus de Nazaré»' in p55_text, "P55 abertura falhou!"
        
        # 2. AUDITAR ENDNOTES.XML
        print("\n" + "-" * 70)
        print("2. AUDITORIA DAS NOTAS FINAIS (word/endnotes.xml)")
        print("-" * 70)
        
        orig_en_tree = ET.fromstring(z_orig.read('word/endnotes.xml'))
        new_en_tree = ET.fromstring(z_new.read('word/endnotes.xml'))
        
        orig_en_notes = [n for n in orig_en_tree.findall('.//w:endnote', NS) if int(n.attrib.get(f'{{{NS["w"]}}}id', 0)) > 0]
        new_en_notes = [n for n in new_en_tree.findall('.//w:endnote', NS) if int(n.attrib.get(f'{{{NS["w"]}}}id', 0)) > 0]
        print(f"[OK] Total de Notas Finais: {len(new_en_notes)} (Esperado: 50)")
        assert len(new_en_notes) == 50, f"Esperado 50 notas, encontrado {len(new_en_notes)}"
        
        ref_markers = new_en_tree.findall('.//w:endnoteRef', NS)
        print(f"[OK] Marcadores Nativos <w:endnoteRef/>: {len(ref_markers)} (Esperado: 50)")
        assert len(ref_markers) == 50, f"Esperado 50 marcadores nativos, encontrado {len(ref_markers)}"
        
        en_t_nodes = new_en_tree.findall('.//w:t', NS)
        new_en_text = ''.join([t.text for t in en_t_nodes if t.text])
        en_straight_d = new_en_text.count('"')
        en_left_curly = new_en_text.count('“')
        en_right_curly = new_en_text.count('”')
        en_ang_left = new_en_text.count('«')
        en_ang_right = new_en_text.count('»')
        
        print(f"[OK] Resíduo de Aspas Duplas nas Notas (<w:t>): {en_straight_d + en_left_curly + en_right_curly} (Esperado: 0)")
        assert (en_straight_d + en_left_curly + en_right_curly) == 0, "Ainda restam aspas duplas nas notas!"
        
        print(f"[OK] Aspas Angulares nas Notas: {en_ang_left} de abertura («) e {en_ang_right} de fechamento (»)")
        print(f"[OK] Balanço Perfeito nas Notas: {en_ang_left == en_ang_right} (Diferença: {abs(en_ang_left - en_ang_right)})")
        assert en_ang_left == en_ang_right, "Aspas nas notas não estão balanceadas!"
        
        # Check P 154 and P 226
        en_paragraphs = new_en_tree.findall('.//w:p', NS)
        p154_text = ''.join(en_paragraphs[154].itertext())
        assert '«filho de Jefoné, o quenezeu»' in p154_text, "P154 não corrigiu par de Jefoné!"
        assert '«no meio dos filhos de Judá»' in p154_text, "P154 não corrigiu par de Judá!"
        print(f"[OK] Nota P 154 (Calebe / Jefoné): Pares exegéticos perfeitamente fechados!")
        
        p226_text = ''.join(en_paragraphs[226].itertext())
        assert '«Yahweh é' in p226_text and 'Servo sofredor»' in p226_text, "P226 não fechou par do Servo sofredor!"
        print(f"[OK] Nota P 226 (Zc 12:10): Pares exegéticos perfeitamente fechados!")
        
        # 3. TESTE DE DIFF TEXTUAL REVERSO
        print("\n" + "-" * 70)
        print("3. TESTE DE DIFF TEXTUAL REVERSO (ZERO ALTERAÇÃO INDEVIDA)")
        print("-" * 70)
        
        def clean_quotes(t):
            for c in '\"“”«»':
                t = t.replace(c, '')
            return t
            
        orig_clean_doc = clean_quotes(''.join([t.text for t in orig_doc_tree.findall('.//w:t', NS) if t.text]))
        new_clean_doc = clean_quotes(''.join([t.text for t in new_doc_tree.findall('.//w:t', NS) if t.text]))
        
        assert orig_clean_doc == new_clean_doc, "Divergência textual detectada no corpo do documento!"
        print("[OK] O corpo do documento é 100% IDÊNTICO letra por letra ao original (exceto as aspas)!")
        
        orig_clean_en = clean_quotes(''.join([t.text for t in orig_en_tree.findall('.//w:t', NS) if t.text]))
        new_clean_en = clean_quotes(''.join([t.text for t in new_en_tree.findall('.//w:t', NS) if t.text]))
        assert orig_clean_en == new_clean_en, "Divergência textual detectada nas notas de fim!"
        print("[OK] As notas de fim são 100% IDÊNTICAS letra por letra ao original (exceto as aspas)!")
        
    print("\n" + "=" * 80)
    print("🏆 AUDITORIA APROVADA COM 100% DE SUCESSO!")
    print("   Todas as aspas foram substituídas por « » com perfeição tipográfica.")
    print("   A integridade estrutural, notas e âncoras permanecem absolutamente invioladas.")
    print("=" * 80)

if __name__ == '__main__':
    run_audit()
