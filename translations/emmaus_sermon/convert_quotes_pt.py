"""
Script de conversão de aspas duplas aéreas (" ", “ ”) para aspas angulares (« »)
na versão em português de 'O Sermão de Emaús' (Versão NVI).

Gera uma cópia independente e preserva 100% da estrutura, formatação,
notas de fim e âncoras.
"""

import os
import zipfile
import xml.etree.ElementTree as ET

SOURCE_DOCX = os.path.join('public', 'downloads', 'O_Sermao_de_Emaus_Versao_NVI_Atualizado.docx')
TARGET_DOCX = os.path.join('translations', 'emmaus_sermon', 'O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.docx')

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
# Register namespace so ET serializes without prefix distortion
ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
ET.register_namespace('m', 'http://schemas.openxmlformats.org/officeDocument/2006/math')
ET.register_namespace('v', 'urn:schemas-microsoft-com:vml')
ET.register_namespace('wp', 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing')
ET.register_namespace('w10', 'urn:schemas-microsoft-com:office:word')
ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
ET.register_namespace('pic', 'http://schemas.openxmlformats.org/drawingml/2006/picture')


def convert_paragraph_text_quotes(text, p_idx, is_endnote=False):
    """
    Converte aspas duplas aéreas em aspas angulares mantendo paridade de tamanho.
    """
    chars = list(text)
    n = len(chars)
    in_quote = False
    
    for i, ch in enumerate(chars):
        if ch == '“':
            chars[i] = '«'
            in_quote = True
        elif ch == '”':
            chars[i] = '»'
            in_quote = False
        elif ch == '"':
            prev_char = chars[i-1] if i > 0 else None
            next_char = chars[i+1] if i + 1 < n else None
            
            if in_quote:
                chars[i] = '»'
                in_quote = False
            else:
                if prev_char is None or prev_char in ' \t\r\n—–([{\':;':
                    if (next_char is None or next_char in ' \t\r\n') and prev_char in ' \t\r\n':
                        chars[i] = '»'
                        in_quote = False
                    else:
                        chars[i] = '«'
                        in_quote = True
                else:
                    chars[i] = '»'
                    in_quote = False

    return ''.join(chars)


def process_xml_part(xml_bytes, is_endnote=False):
    root = ET.fromstring(xml_bytes)
    paragraphs = root.findall('.//w:p', NS)
    
    for p_idx, p in enumerate(paragraphs):
        t_nodes = p.findall('.//w:t', NS)
        if not t_nodes:
            continue
            
        orig_text = ''.join([t.text for t in t_nodes if t.text])
        if not any(c in orig_text for c in ['"', '“', '”']):
            continue

        # Special cases for endnotes P 154 and P 226 (Option A: balance pre-existing missing quotes)
        if is_endnote and p_idx == 154:
            for t in t_nodes:
                if t.text and 'chamado  filho de Jefoné, o quenezeu"' in t.text:
                    t.text = t.text.replace('chamado  filho de Jefoné, o quenezeu"', 'chamado  «filho de Jefoné, o quenezeu»')
                if t.text and '"no meio dos filhos de Judá"' in t.text:
                    t.text = t.text.replace('"no meio dos filhos de Judá"', '«no meio dos filhos de Judá»')
            continue

        if is_endnote and p_idx == 226:
            for t in t_nodes:
                if t.text and '"Yahweh é' in t.text:
                    t.text = t.text.replace('"Yahweh é', '«Yahweh é')
                if t.text and 'Servo sofredor.' in t.text:
                    t.text = t.text.replace('Servo sofredor.', 'Servo sofredor».')
            continue

        # General standard replacement
        conv_text = convert_paragraph_text_quotes(orig_text, p_idx, is_endnote=is_endnote)
        
        # Verify length parity
        if len(conv_text) == len(orig_text):
            offset = 0
            for t in t_nodes:
                if t.text:
                    l = len(t.text)
                    t.text = conv_text[offset : offset + l]
                    offset += l
        else:
            raise ValueError(f"Tamanho incompatível no parágrafo {p_idx}: {len(orig_text)} vs {len(conv_text)}")

    return ET.tostring(root, encoding='utf-8', xml_declaration=True)


def convert_quotes():
    print(f"Iniciando conversão de aspas...")
    print(f"Origem:  {SOURCE_DOCX}")
    print(f"Destino: {TARGET_DOCX}")
    
    os.makedirs(os.path.dirname(TARGET_DOCX), exist_ok=True)
    
    with zipfile.ZipFile(SOURCE_DOCX, 'r') as zin, zipfile.ZipFile(TARGET_DOCX, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            content = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                print(f"Processando word/document.xml...")
                content = process_xml_part(content, is_endnote=False)
            elif item.filename == 'word/endnotes.xml':
                print(f"Processando word/endnotes.xml...")
                content = process_xml_part(content, is_endnote=True)
            zout.writestr(item, content)

    print(f"Conversão concluída com sucesso em {TARGET_DOCX}!")

if __name__ == '__main__':
    convert_quotes()

