# -*- coding: utf-8 -*-
import json
import re

pt_p = json.load(open('translations/emmaus_sermon/source_pt_formatted_paragraphs.json', encoding='utf-8'))
es_p = json.load(open('translations/emmaus_sermon/es_final_paragraphs.json', encoding='utf-8'))
en_p = json.load(open('translations/emmaus_sermon/en_final_paragraphs.json', encoding='utf-8'))

print("=== AUDIT OF ANCHOR POSITIONS (EN_REF:1 to 50) ===")
anchor_issues = []

for i in range(1, 51):
    tag = f"[EN_REF:{i}]"
    pt_found = [(idx, p['text']) for idx, p in enumerate(pt_p) if tag in p['text']]
    es_found = [(idx, p['text']) for idx, p in enumerate(es_p) if tag in p['text']]
    en_found = [(idx, p['text']) for idx, p in enumerate(en_p) if tag in p['text']]
    
    if not pt_found:
        print(f"Warning: {tag} not found in PT!")
        continue
        
    p_idx = pt_found[0][0]
    pt_text = pt_found[0][1]
    es_text = es_found[0][1] if es_found else "NOT FOUND"
    en_text = en_found[0][1] if en_found else "NOT FOUND"
    
    # Check if anchor is at end of paragraph in PT vs ES vs EN
    pt_at_end = pt_text.strip().endswith(tag) or pt_text.strip().endswith(tag + '"') or pt_text.strip().endswith(tag + '.')
    es_at_end = es_text.strip().endswith(tag) or es_text.strip().endswith(tag + '"') or es_text.strip().endswith(tag + '.')
    en_at_end = en_text.strip().endswith(tag) or en_text.strip().endswith(tag + '"') or en_text.strip().endswith(tag + '.')
    
    # If PT is NOT at end, but ES or EN IS at end (or vice-versa, or adjacent to another tag)
    # Get surrounding text in PT (30 chars before)
    pos_pt = pt_text.find(tag)
    context_pt = pt_text[max(0, pos_pt-30):pos_pt]
    
    pos_es = es_text.find(tag)
    context_es = es_text[max(0, pos_es-30):pos_es] if pos_es != -1 else ""
    
    pos_en = en_text.find(tag)
    context_en = en_text[max(0, pos_en-30):pos_en] if pos_en != -1 else ""
    
    # Is it clustered with another EN_REF?
    clustered_es = bool(re.search(r'\[EN_REF:\d+\]\[EN_REF:\d+\]', es_text))
    clustered_en = bool(re.search(r'\[EN_REF:\d+\]\[EN_REF:\d+\]', en_text))
    
    print(f"\nNote {i} (P{p_idx}):")
    print(f"  PT context: ...{context_pt} -> {tag}")
    print(f"  ES context: ...{context_es} -> {tag}")
    print(f"  EN context: ...{context_en} -> {tag}")
    if (not pt_at_end and (es_at_end or en_at_end)) or (tag in es_text and '[EN_REF:' in es_text[pos_es+len(tag):pos_es+len(tag)+15]):
        print(f"  >>> MISALIGNMENT DETECTED for Note {i}!")
        anchor_issues.append(i)

print(f"\nTotal notes with misplaced anchors: {len(anchor_issues)}: {anchor_issues}")
