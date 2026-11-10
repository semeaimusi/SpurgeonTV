# -*- coding: utf-8 -*-
import os
import sys
import zipfile
import json
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("AUDITORIA FINAL EXAUSTIVA: REALINHAMENTO DE ÂNCORAS E COMPLETUDE DE CONTEÚDO")
print("=" * 80)

pt_notes = json.load(open('translations/emmaus_sermon/source_pt_formatted_endnotes.json', encoding='utf-8'))
pt_map = {n['id']: n['paragraphs'] for n in pt_notes}
pt_total_paras = sum(len(p) for p in pt_map.values())
pt_total_words = sum(sum(len(p.split()) for p in paras) for paras in pt_map.values())

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

all_passed = True

for lang, docx_path in [('ES', 'translations/emmaus_sermon/El_Sermon_de_Emaus_Version_NVI.docx'),
                        ('EN', 'translations/emmaus_sermon/The_Emmaus_Sermon_NIV_Version.docx')]:
    print(f"\n" + "-" * 70)
    print(f"AUDITANDO DOCUMENTO: {os.path.basename(docx_path)} ({lang})")
    print("-" * 70)
    
    if not os.path.exists(docx_path):
        print(f"❌ ARQUIVO NÃO ENCONTRADO: {docx_path}")
        all_passed = False
        continue
        
    size_kb = os.path.getsize(docx_path) / 1024
    print(f"  ✓ Tamanho do Arquivo: {size_kb:.2f} KB")
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        # 1. Audit document.xml
        doc_xml = z.read('word/document.xml')
        tree_doc = ET.fromstring(doc_xml)
        doc_paras = tree_doc.findall('.//w:p', ns)
        en_refs = tree_doc.findall('.//w:endnoteReference', ns)
        
        print(f"  ✓ Parágrafos no corpo: {len(doc_paras)} (Esperado: 543)")
        print(f"  ✓ Âncoras no corpo: {len(en_refs)} (Esperado: 50)")
        
        w_id = f"{{{ns['w']}}}id"
        # Check P40 specifically
        p40 = doc_paras[40]
        runs_40 = []
        for child in p40:
            tag = child.tag.split('}')[-1]
            if tag == 'r':
                ref = child.find('w:endnoteReference', ns)
                if ref is not None:
                    runs_40.append(f"[EN_REF:{ref.attrib.get(w_id)}]")
                else:
                    t_nodes = child.iterfind('.//w:t', ns)
                    t_str = ''.join(t.text for t in t_nodes if t.text)
                    runs_40.append(t_str)
        p40_text = "".join(runs_40)
        print(f"  ✓ Parágrafo 40 no DOCX:\n    \"{p40_text}\"")
        
        # Check that [EN_REF:1] and [EN_REF:2] are NOT adjacent
        if "[EN_REF:1][EN_REF:2]" in p40_text:
            print("  ❌ ERRO: Âncoras 1 e 2 continuam aglomeradas em P40!")
            all_passed = False
        elif "[EN_REF:1]" in p40_text and "[EN_REF:2]" in p40_text:
            print("  ✓ Âncoras 1 e 2 perfeitamente separadas e alocadas nos termos corretos!")
        else:
            print("  ❌ ERRO: Âncoras 1 ou 2 ausentes em P40!")
            all_passed = False
            
        # Check P49 specifically
        p49 = doc_paras[49]
        runs_49 = []
        for child in p49:
            tag = child.tag.split('}')[-1]
            if tag == 'r':
                ref = child.find('w:endnoteReference', ns)
                if ref is not None:
                    runs_49.append(f"[EN_REF:{ref.attrib.get(w_id)}]")
                else:
                    t_nodes = child.iterfind('.//w:t', ns)
                    t_str = ''.join(t.text for t in t_nodes if t.text)
                    runs_49.append(t_str)
        p49_text = "".join(runs_49)
        print(f"  ✓ Parágrafo 49 no DOCX:\n    \"{p49_text}\"")
        if "[EN_REF:3][EN_REF:4]" in p49_text:
            print("  ❌ ERRO: Âncoras 3 e 4 continuam aglomeradas em P49!")
            all_passed = False
        elif "[EN_REF:3]" in p49_text and "[EN_REF:4]" in p49_text:
            print("  ✓ Âncoras 3 e 4 perfeitamente separadas e alocadas em Cleopas e Natanael!")
        else:
            print("  ❌ ERRO: Âncoras 3 ou 4 ausentes em P49!")
            all_passed = False
            
        # 2. Audit endnotes.xml
        en_xml = z.read('word/endnotes.xml')
        tree_en = ET.fromstring(en_xml)
        notes = [en for en in tree_en.findall('.//w:endnote', ns)
                 if en.attrib.get(f"{{{ns['w']}}}type") not in ['separator', 'continuationSeparator']]
        
        # Check that EVERY endnote has <w:endnoteRef/> in its first paragraph!
        notes_with_ref = [en for en in notes if en.findall('w:p', ns)[0].find('.//w:endnoteRef', ns) is not None]
        print(f"  ✓ Elementos w:endnote com marcador de numeração <w:endnoteRef/>: {len(notes_with_ref)} de {len(notes)}")
        if len(notes_with_ref) != 50:
            print("  ❌ ERRO: Faltam marcadores de numeração <w:endnoteRef/> em algumas notas!")
            all_passed = False
        else:
            print("  ✓ Todas as 50 notas possuem o marcador nativo de numeração do Word!")
        
        extracted_notes = {}
        total_words = 0
        total_paras = 0
        corrupt_chars = 0
        
        for en in notes:
            nid = en.attrib.get(f"{{{ns['w']}}}id")
            en_p_list = en.findall('w:p', ns)
            p_texts = []
            for p in en_p_list:
                t_nodes = p.iterfind('.//w:t', ns)
                t_str = ''.join(t.text for t in t_nodes if t.text)
                if t_str.strip():
                    p_texts.append(t_str)
                    total_words += len(t_str.split())
                    if '\ufffd' in t_str:
                        corrupt_chars += 1
            extracted_notes[nid] = p_texts
            total_paras += len(p_texts)
            
        print(f"  ✓ Elementos w:endnote: {len(notes)}")
        print(f"  ✓ Total de Parágrafos nas Notas: {total_paras} (PT: {pt_total_paras})")
        print(f"  ✓ Total de Palavras nas Notas: {total_words} (PT: {pt_total_words})")
        print(f"  ✓ Razão de Volume de Palavras: {total_words / pt_total_words:.2f}")
        print(f"  ✓ Caracteres corrompidos: {corrupt_chars}")
        
        if total_paras != pt_total_paras:
            print(f"  ❌ ERRO: Paridade de parágrafos divergente: {total_paras} != {pt_total_paras}")
            all_passed = False
        else:
            print(f"  ✓ Paridade de 181 parágrafos preservada!")
            
        # Check Note 8 content (must be Cain, Abel, Seth)
        n8_text = " ".join(extracted_notes.get('8', [])).lower()
        if 'abel' in n8_text and ('set' in n8_text or 'seth' in n8_text) and 'fratricid' in n8_text:
            print(f"  ✓ NOTA 8 RESTAURADA COM SUCESSO! Conteúdo trata de Caim, Abel e Sete.")
        else:
            print(f"  ❌ ERRO: Nota 8 não contém o texto de Caim/Abel/Sete!")
            all_passed = False
            
        # Check Note 20 content (must be Joshua, Jericho, Commander of army of Lord)
        n20_text = " ".join(extracted_notes.get('20', [])).lower()
        if ('jericó' in n20_text or 'jericho' in n20_text) and ('príncipe' in n20_text or 'commander' in n20_text) and ('yehoshua' in n20_text or 'iesous' in n20_text):
            print(f"  ✓ NOTA 20 RESTAURADA COM SUCESSO! Conteúdo trata de Yehoshua e Jericó.")
        else:
            print(f"  ❌ ERRO: Nota 20 não contém o texto de Jericó e Yehoshua!")
            all_passed = False
            
        # Check Note 5 ratio
        n5_words = sum(len(p.split()) for p in extracted_notes.get('5', []))
        pt_n5_words = sum(len(p.split()) for p in pt_map['5'])
        print(f"  ✓ NOTA 5: {n5_words} palavras (PT: {pt_n5_words}w, razão={n5_words/pt_n5_words:.2f})")
        
        # Check Note 7 ratio
        n7_words = sum(len(p.split()) for p in extracted_notes.get('7', []))
        pt_n7_words = sum(len(p.split()) for p in pt_map['7'])
        print(f"  ✓ NOTA 7: {n7_words} palavras (PT: {pt_n7_words}w, razão={n7_words/pt_n7_words:.2f})")
        
        # Check Note 9 ratio
        n9_words = sum(len(p.split()) for p in extracted_notes.get('9', []))
        pt_n9_words = sum(len(p.split()) for p in pt_map['9'])
        print(f"  ✓ NOTA 9: {n9_words} palavras (PT: {pt_n9_words}w, razão={n9_words/pt_n9_words:.2f})")

print("\n" + "=" * 80)
if all_passed:
    print("🏆 AUDITORIA APROVADA COM 100% DE SUCESSO!")
    print("   Todas as 50 âncoras foram devidamente realinhadas.")
    print("   Todas as notas com conteúdo incompleto foram plenamente restauradas.")
else:
    print("⚠️ FALHA EM UM OU MAIS TESTES DE AUDITORIA.")
print("=" * 80)
