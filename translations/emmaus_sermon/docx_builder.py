# -*- coding: utf-8 -*-
import sys
import os
import re
import json
import zipfile
import shutil
import xml.etree.ElementTree as ET

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace('w', W_NS)

def parse_runs_from_text(formatted_text):
    # Pattern to match tokens: [EN_REF:id], ***bold italic***, **bold**, *italic*, or plain text
    # Let's tokenize using regex
    token_pattern = re.compile(
        r'(\[EN_REF:\d+\])'
        r'|(\*\*\*[^*]+?\*\*\*)'
        r'|(\*\*[^*]+?\*\*)'
        r'|(\*[^*]+?\*)'
        r'|([^*\[]+|\[(?!EN_REF:\d+\])|\*)'
    )
    
    runs = []
    pos = 0
    while pos < len(formatted_text):
        m = token_pattern.match(formatted_text, pos)
        if not m:
            # Fallback one character
            runs.append({'type': 'text', 'text': formatted_text[pos], 'b': False, 'i': False})
            pos += 1
            continue
            
        full_match = m.group(0)
        pos = m.end()
        
        if m.group(1): # [EN_REF:id]
            en_id = re.search(r'\d+', full_match).group(0)
            runs.append({'type': 'endnote_ref', 'id': en_id})
        elif m.group(2): # ***bold italic***
            text_inside = full_match[3:-3]
            runs.append({'type': 'text', 'text': text_inside, 'b': True, 'i': True})
        elif m.group(3): # **bold**
            text_inside = full_match[2:-2]
            runs.append({'type': 'text', 'text': text_inside, 'b': True, 'i': False})
        elif m.group(4): # *italic*
            text_inside = full_match[1:-1]
            runs.append({'type': 'text', 'text': text_inside, 'b': False, 'i': True})
        else:
            runs.append({'type': 'text', 'text': full_match, 'b': False, 'i': False})
            
    return runs

def create_run_element(run_info, default_rPr=None):
    r = ET.Element(f'{{{W_NS}}}r')
    
    if run_info['type'] == 'endnote_ref':
        rPr = ET.SubElement(r, f'{{{W_NS}}}rPr')
        rStyle = ET.SubElement(rPr, f'{{{W_NS}}}rStyle')
        rStyle.attrib[f'{{{W_NS}}}val'] = 'Textodenotadefim'
        en_ref = ET.SubElement(r, f'{{{W_NS}}}endnoteReference')
        en_ref.attrib[f'{{{W_NS}}}id'] = str(run_info['id'])
        return r
        
    rPr = None
    if default_rPr is not None:
        rPr = ET.fromstring(ET.tostring(default_rPr))
        # remove existing b and i from copied rPr so we can set them accurately
        for tag in ['b', 'i', 'bCs', 'iCs']:
            node = rPr.find(f'{{{W_NS}}}{tag}')
            if node is not None:
                rPr.remove(node)
    
    if run_info.get('b') or run_info.get('i'):
        if rPr is None:
            rPr = ET.Element(f'{{{W_NS}}}rPr')
        if run_info.get('b'):
            ET.SubElement(rPr, f'{{{W_NS}}}b')
        if run_info.get('i'):
            ET.SubElement(rPr, f'{{{W_NS}}}i')
            
    if rPr is not None and len(rPr) > 0:
        r.append(rPr)
        
    t = ET.SubElement(r, f'{{{W_NS}}}t')
    text_val = run_info['text']
    t.text = text_val
    if text_val.startswith(' ') or text_val.endswith(' ') or '  ' in text_val:
        t.attrib['{http://www.w3.org/XML/1998/namespace}space'] = 'preserve'
        
    return r

def build_docx_from_data(paragraphs_data, endnotes_data, output_docx_path, template_docx_path=r'public/downloads/O_Sermao_de_Emaus_Versao_NVI_Atualizado.docx'):
    # Endnotes lookup
    endnotes_map = {str(n['id']): n['paragraphs'] for n in endnotes_data}
    
    temp_dir = os.path.join('translations/emmaus_sermon', 'temp_docx_build')
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    with zipfile.ZipFile(template_docx_path, 'r') as z:
        z.extractall(temp_dir)
        
    # 1. Process document.xml
    doc_xml_path = os.path.join(temp_dir, 'word', 'document.xml')
    tree_doc = ET.parse(doc_xml_path)
    root_doc = tree_doc.getroot()
    ns = {'w': W_NS}
    
    all_p = root_doc.findall('.//w:p', ns)
    
    for idx, p_data in enumerate(paragraphs_data):
        if idx >= len(all_p):
            break
        p = all_p[idx]
        formatted_text = p_data['text']
        
        # Get first run rPr as default style template if available
        first_r = p.find('w:r', ns)
        default_rPr = None
        if first_r is not None:
            default_rPr = first_r.find('w:rPr', ns)
            
        # Keep only pPr
        pPr = p.find('w:pPr', ns)
        # Remove all existing elements from p
        p.clear()
        if pPr is not None:
            p.append(pPr)
            
        if not formatted_text:
            continue
            
        runs_info = parse_runs_from_text(formatted_text)
        for r_info in runs_info:
            r_elem = create_run_element(r_info, default_rPr)
            p.append(r_elem)
            
    tree_doc.write(doc_xml_path, encoding='utf-8', xml_declaration=True)
    
    # 2. Process endnotes.xml
    endnotes_xml_path = os.path.join(temp_dir, 'word', 'endnotes.xml')
    tree_en = ET.parse(endnotes_xml_path)
    root_en = tree_en.getroot()
    
    for en in root_en.findall('.//w:endnote', ns):
        en_id = en.attrib.get(f'{{{W_NS}}}id')
        en_type = en.attrib.get(f'{{{W_NS}}}type')
        if en_type in ['separator', 'continuationSeparator']:
            continue
        if str(en_id) in endnotes_map:
            new_note_paragraphs = endnotes_map[str(en_id)]
            existing_p = en.findall('w:p', ns)
            
            # Default style templates
            default_pPr = None
            default_rPr = None
            if existing_p:
                pPr_node = existing_p[0].find('w:pPr', ns)
                if pPr_node is not None:
                    default_pPr = ET.fromstring(ET.tostring(pPr_node))
                first_r = existing_p[0].find('w:r', ns)
                if first_r is not None:
                    rPr_node = first_r.find('w:rPr', ns)
                    if rPr_node is not None:
                        default_rPr = ET.fromstring(ET.tostring(rPr_node))
                        
            # Remove any excess existing paragraphs that are beyond the target paragraph count
            while len(existing_p) > len(new_note_paragraphs):
                p_to_remove = existing_p.pop()
                en.remove(p_to_remove)
                
            for p_idx, new_p_text in enumerate(new_note_paragraphs):
                if p_idx < len(existing_p):
                    target_p = existing_p[p_idx]
                else:
                    target_p = ET.SubElement(en, f'{{{W_NS}}}p')
                    
                pPr = target_p.find('w:pPr', ns)
                first_r = target_p.find('w:r', ns)
                curr_rPr = first_r.find('w:rPr', ns) if first_r is not None else default_rPr
                
                target_p.clear()
                if pPr is not None:
                    target_p.append(pPr)
                elif default_pPr is not None:
                    target_p.append(ET.fromstring(ET.tostring(default_pPr)))
                    
                # If this is the FIRST paragraph of the endnote, insert the Word endnote reference marker!
                if p_idx == 0:
                    ref_r = ET.SubElement(target_p, f'{{{W_NS}}}r')
                    ref_rPr = ET.SubElement(ref_r, f'{{{W_NS}}}rPr')
                    ref_rStyle = ET.SubElement(ref_rPr, f'{{{W_NS}}}rStyle')
                    ref_rStyle.attrib[f'{{{W_NS}}}val'] = 'Refdenotadefim'
                    ET.SubElement(ref_r, f'{{{W_NS}}}endnoteRef')
                    
                    space_r = ET.SubElement(target_p, f'{{{W_NS}}}r')
                    space_t = ET.SubElement(space_r, f'{{{W_NS}}}t')
                    space_t.attrib['{http://www.w3.org/XML/1998/namespace}space'] = 'preserve'
                    space_t.text = ' '
                    
                runs_info = parse_runs_from_text(new_p_text)
                for r_info in runs_info:
                    r_elem = create_run_element(r_info, curr_rPr)
                    target_p.append(r_elem)
                    
    tree_en.write(endnotes_xml_path, encoding='utf-8', xml_declaration=True)
    
    # 3. Repackage into output docx
    os.makedirs(os.path.dirname(output_docx_path), exist_ok=True)
    with zipfile.ZipFile(output_docx_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, temp_dir)
                z_out.write(filepath, arcname)
                
    shutil.rmtree(temp_dir)
    print(f"Successfully generated DOCX at {output_docx_path}!")

if __name__ == '__main__':
    # Test roundtrip with source pt
    with open('translations/emmaus_sermon/source_pt_formatted_paragraphs.json', 'r', encoding='utf-8') as f:
        p_data = json.load(f)
    with open('translations/emmaus_sermon/source_pt_formatted_endnotes.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
        
    test_out = 'translations/emmaus_sermon/test_roundtrip.docx'
    build_docx_from_data(p_data, en_data, test_out)
