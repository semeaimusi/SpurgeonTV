"""
Conversor de alta precisão de DOCX para EPUB 3.0 (com retrocompatibilidade EPUB 2 NCX)
para a obra:
'O Sermão de Emaús: Você Conhece as Promessas Messiânicas do Antigo Testamento?'
Arquivo de origem: translations/emmaus_sermon/O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.docx
Arquivo de destino: translations/emmaus_sermon/O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.epub
"""

import os
import sys
import re
import html
import zipfile
import xml.etree.ElementTree as ET

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

SOURCE_DOCX = os.path.join('translations', 'emmaus_sermon', 'O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.docx')
COVER_JPG = os.path.join('public', 'images', 'store', 'o_sermao_de_emaus.jpg')
TARGET_EPUB = os.path.join('translations', 'emmaus_sermon', 'O_Sermao_de_Emaus_Versao_NVI_Atualizado_Aspas_Angulares.epub')

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W_VAL = f'{{{NS["w"]}}}val'
W_ID = f'{{{NS["w"]}}}id'
W_TYPE = f'{{{NS["w"]}}}type'
W_LEFT = f'{{{NS["w"]}}}left'
W_FIRST = f'{{{NS["w"]}}}firstLine'


def is_on(elem):
    if elem is None:
        return False
    val = elem.attrib.get(W_VAL, 'true').lower()
    return val not in ('0', 'false', 'none', 'off')


def linkify_text(escaped_text):
    """Converte URLs e e-mails em links clicáveis preservando XHTML."""
    # Linkify URLs
    url_pattern = re.compile(r'(https?://[^\s<>"]+[^\s<>".,;!)])')
    escaped_text = url_pattern.sub(r'<a href="\1">\1</a>', escaped_text)
    # Linkify known emails if not already linked
    for email in ('webert@ymail.com', 'semeaigospel@gmail.com'):
        if email in escaped_text and f'mailto:{email}' not in escaped_text:
            escaped_text = escaped_text.replace(email, f'<a href="mailto:{email}">{email}</a>')
    return escaped_text


def render_run_children(r, anchor_map=None, current_file=None, skip_endnote_ref_tag=False):
    """Converte um elemento <w:r> em XHTML."""
    rPr = r.find('w:rPr', NS)
    bold = is_on(rPr.find('w:b', NS)) if rPr is not None else False
    italic = is_on(rPr.find('w:i', NS)) if rPr is not None else False
    underline = is_on(rPr.find('w:u', NS)) if rPr is not None else False
    vert = rPr.find('w:vertAlign', NS) if rPr is not None else None
    is_sup = (vert is not None and vert.attrib.get(W_VAL) == 'superscript')

    # Ignorar <w:instrText>
    if r.find('w:instrText', NS) is not None:
        return ''

    parts = []
    for child in r:
        tag = child.tag.split('}')[-1]
        if tag == 't' and child.text:
            txt = child.text
            escaped = html.escape(txt, quote=False)
            parts.append(escaped)
        elif tag == 'br':
            br_type = child.attrib.get(W_TYPE, '')
            if br_type == 'page':
                parts.append('<!--PAGE_BREAK-->')
            else:
                parts.append('<br/>')
        elif tag == 'endnoteReference':
            eid = child.attrib.get(W_ID, '')
            if eid and int(eid) > 0:
                if anchor_map is not None and current_file is not None:
                    anchor_map[int(eid)] = current_file
                parts.append(
                    f'<sup class="endnote-ref"><a id="ref{eid}" href="notas_finais.xhtml#fn{eid}" epub:type="noteref">{eid}</a></sup>'
                )
        elif tag == 'endnoteRef':
            if not skip_endnote_ref_tag:
                parts.append('<!--ENDNOTE_REF-->')

    inner = ''.join(parts)
    if not inner or inner in ('<!--PAGE_BREAK-->', '<!--ENDNOTE_REF-->'):
        return inner

    # Se contiver <!--PAGE_BREAK-->, aplicar formatação apenas nos lados
    if '<!--PAGE_BREAK-->' in inner:
        subparts = inner.split('<!--PAGE_BREAK-->')
        formatted_subs = []
        for sp in subparts:
            if sp:
                res = sp
                if underline:
                    res = f'<u>{res}</u>'
                if italic:
                    res = f'<em>{res}</em>'
                if bold:
                    res = f'<strong>{res}</strong>'
                if is_sup:
                    res = f'<sup>{res}</sup>'
                formatted_subs.append(res)
            else:
                formatted_subs.append('')
        return '<!--PAGE_BREAK-->'.join(formatted_subs)

    res = inner
    if underline:
        res = f'<u>{res}</u>'
    if italic:
        res = f'<em>{res}</em>'
    if bold:
        res = f'<strong>{res}</strong>'
    if is_sup:
        res = f'<sup>{res}</sup>'
    return res


def render_paragraph_inner(p, anchor_map=None, current_file=None, fix_p421=False, skip_endnote_ref_tag=False):
    """Renderiza o conteúdo interno de um parágrafo <w:p> em XHTML."""
    chunks = []
    for child in p:
        tag = child.tag.split('}')[-1]
        if tag == 'r':
            chunks.append(render_run_children(child, anchor_map, current_file, skip_endnote_ref_tag))
        elif tag == 'hyperlink':
            for sub_r in child.findall('.//w:r', NS):
                chunks.append(render_run_children(sub_r, anchor_map, current_file, skip_endnote_ref_tag))

    combined = ''.join(chunks)
    if fix_p421 and combined.startswith('»E quanto a Jeremias'):
        combined = '«E quanto a Jeremias' + combined[len('»E quanto a Jeremias'):]
    elif fix_p421 and '»E quanto a Jeremias' in combined:
        combined = combined.replace('»E quanto a Jeremias', '«E quanto a Jeremias', 1)

    # Limpar tags adjacentes redundantes (ex: </strong><strong>, </em><em>)
    for tag_name in ('strong', 'em', 'u', 'sup'):
        combined = combined.replace(f'</{tag_name}><{tag_name}>', '')

    combined = linkify_text(combined)
    return combined


def get_paragraph_plain_text(p):
    t_nodes = p.findall('.//w:t', NS)
    return ''.join([t.text for t in t_nodes if t.text]).strip()


def get_paragraph_style_and_indent(p):
    pPr = p.find('w:pPr', NS)
    pStyle = pPr.find('w:pStyle', NS) if pPr is not None else None
    style_val = pStyle.attrib.get(W_VAL) if pStyle is not None else 'Normal'

    jc = pPr.find('w:jc', NS) if pPr is not None else None
    jc_val = jc.attrib.get(W_VAL) if jc is not None else ''

    ind = pPr.find('w:ind', NS) if pPr is not None else None
    left_ind = int(ind.attrib.get(W_LEFT, '0')) if ind is not None and ind.attrib.get(W_LEFT, '0').isdigit() else 0
    first_ind = int(ind.attrib.get(W_FIRST, '0')) if ind is not None and ind.attrib.get(W_FIRST, '0').isdigit() else 0

    return style_val, jc_val, left_ind, first_ind


def wrap_xhtml_document(title, body_html, lang='pt-BR'):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{lang}" lang="{lang}">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="styles/stylesheet.css" />
</head>
<body>
{body_html}
</body>
</html>
'''


STYLESHEET_CSS = '''/* Folha de Estilo Editorial Clássica - O Sermão de Emaús (EPUB 3.0) */

body {
  font-family: "Garamond", "Georgia", "Palatino Linotype", "Book Antiqua", serif;
  line-height: 1.62;
  margin: 4% 5%;
  text-align: justify;
}

/* Capa e Folha de Rosto */
.cover-container {
  text-align: center;
  margin: 0;
  padding: 0;
  page-break-inside: avoid;
}
.cover-container img {
  max-width: 100%;
  max-height: 95vh;
  height: auto;
  width: auto;
}

.title-page {
  text-align: center;
  margin-top: 10%;
  margin-bottom: 10%;
}
.book-title {
  font-size: 2.2em;
  font-weight: bold;
  letter-spacing: 0.04em;
  margin-bottom: 0.4em;
  text-align: center;
  line-height: 1.2;
}
.book-subtitle {
  font-size: 1.25em;
  font-style: italic;
  margin-bottom: 1.5em;
  text-align: center;
  line-height: 1.35;
}
.book-description {
  font-size: 1em;
  margin: 1.5em auto;
  max-width: 90%;
  text-align: center;
}
.book-epigraph {
  font-size: 1.05em;
  font-style: italic;
  margin: 2.5em 8% 1.5em 8%;
  padding: 1em;
  border-top: 1px solid #888;
  border-bottom: 1px solid #888;
  text-align: center;
}

/* Ficha Catalográfica e Créditos */
.cip-section {
  font-size: 0.88em;
  line-height: 1.45;
  margin-top: 1.5em;
}
.cip-box {
  border: 1px solid #777;
  padding: 1.2em;
  margin: 1.2em 0;
  text-align: left;
}
.cip-header {
  font-weight: bold;
  text-align: center;
  margin-bottom: 0.8em;
  font-size: 1.05em;
}
.cip-line {
  text-indent: 0;
  margin: 0.25em 0;
  text-align: left;
}
.legal-heading {
  font-weight: bold;
  font-size: 1.02em;
  margin-top: 1.4em;
  margin-bottom: 0.3em;
  text-indent: 0;
  text-align: left;
}

/* Títulos e Cabeçalhos */
h1.part-title {
  font-size: 1.55em;
  font-weight: bold;
  text-align: center;
  margin-top: 2em;
  margin-bottom: 1.5em;
  padding-bottom: 0.4em;
  border-bottom: 2px solid #2C3E50;
  line-height: 1.3;
  page-break-after: avoid;
}

h2.section-title {
  font-size: 1.22em;
  font-weight: bold;
  text-align: left;
  margin-top: 1.8em;
  margin-bottom: 0.8em;
  line-height: 1.35;
  page-break-after: avoid;
}

h3.sub-heading {
  font-size: 1.08em;
  font-weight: bold;
  text-align: left;
  margin-top: 1.3em;
  margin-bottom: 0.4em;
  text-indent: 0;
  page-break-after: avoid;
}

/* Parágrafos Narrativos e Citações */
p {
  margin-top: 0;
  margin-bottom: 0.45em;
  text-align: justify;
}
p.indent {
  text-indent: 1.5em;
}
p.no-indent {
  text-indent: 0;
}
p.center {
  text-align: center;
  text-indent: 0;
}
p.blockquote {
  margin-left: 1.8em;
  margin-right: 1em;
  margin-top: 0.6em;
  margin-bottom: 0.6em;
  text-indent: 0;
}

/* Índice de Versículos Messiânicos */
.verse-index-item {
  margin-top: 0.7em;
  margin-bottom: 0.9em;
  padding-left: 0.8em;
  border-left: 3px solid #2C3E50;
  text-indent: 0;
  text-align: left;
  line-height: 1.48;
}

/* Notas Finais e Âncoras */
sup.endnote-ref {
  font-size: 0.78em;
  line-height: 0;
  vertical-align: super;
  margin-left: 0.08em;
}
sup.endnote-ref a {
  text-decoration: none;
  font-weight: bold;
}

.endnote-item {
  display: block;
  margin-top: 1em;
  margin-bottom: 1.2em;
  padding-bottom: 0.6em;
  border-bottom: 1px dotted #ccc;
}
.endnote-item p {
  font-size: 0.94em;
  line-height: 1.52;
  margin-bottom: 0.4em;
}
.endnote-number {
  font-weight: bold;
  margin-right: 0.35em;
  text-decoration: none;
}
.endnote-backref {
  margin-left: 0.4em;
  text-decoration: none;
  font-size: 0.9em;
}

/* Bibliografia */
p.bib-entry {
  padding-left: 1.8em;
  text-indent: -1.8em;
  margin-top: 0.4em;
  margin-bottom: 0.65em;
  font-size: 0.92em;
  line-height: 1.48;
  text-align: left;
}

/* Sumário Interativo */
nav#toc ol, .toc-list {
  list-style-type: none;
  padding-left: 0;
}
nav#toc ol ol, .toc-sublist {
  list-style-type: none;
  padding-left: 1.4em;
  margin-top: 0.25em;
  margin-bottom: 0.6em;
}
.toc-part {
  font-weight: bold;
  margin-top: 0.9em;
  margin-bottom: 0.3em;
  text-indent: 0;
  text-align: left;
}
.toc-sec {
  margin-top: 0.2em;
  margin-bottom: 0.2em;
  font-weight: normal;
  font-size: 0.95em;
  text-indent: 0;
  text-align: left;
}
nav#toc a, .toc-list a {
  text-decoration: none;
}
'''


def build_epub():
    print("=" * 80)
    print("CONSTRUINDO EPUB 3.0: O SERMÃO DE EMAÚS (VERSÃO NVI - ASPAS ANGULARES)")
    print("=" * 80)

    with zipfile.ZipFile(SOURCE_DOCX, 'r') as z:
        doc_tree = ET.fromstring(z.read('word/document.xml'))
        en_tree = ET.fromstring(z.read('word/endnotes.xml'))

    paragraphs = doc_tree.findall('.//w:p', NS)
    print(f"Total de parágrafos lidos de document.xml: {len(paragraphs)}")

    # Mapa de onde cada âncora (1..50) está localizada (arquivo XHTML)
    anchor_map = {}

    # 1. CAPA (cover.xhtml)
    cover_html = wrap_xhtml_document(
        "Capa - O Sermão de Emaús",
        '''<div class="cover-container" epub:type="cover">
  <img src="images/cover.jpg" alt="Capa: O Sermão de Emaús - Você Conhece as Promessas Messiânicas do Antigo Testamento? - Webert T. S. Costa" />
</div>'''
    )

    # 2. FOLHA DE ROSTO (rosto.xhtml) - P 0 a P 4
    p0 = render_paragraph_inner(paragraphs[0])
    p1 = render_paragraph_inner(paragraphs[1])
    p2 = render_paragraph_inner(paragraphs[2])
    p4 = render_paragraph_inner(paragraphs[4]).replace('<!--PAGE_BREAK-->', '')
    rosto_body = f'''<section epub:type="titlepage" class="title-page">
  <div class="book-title">{p0}</div>
  <div class="book-subtitle">{p1}</div>
  <p class="book-description">{p2}</p>
  <div class="book-epigraph">{p4}</div>
</section>'''
    rosto_html = wrap_xhtml_document("Folha de Rosto", rosto_body)

    # 3. FICHA CATALOGRÁFICA E CRÉDITOS (creditos.xhtml) - P 5 a P 31
    creditos_lines = ['<section epub:type="copyright-page" class="cip-section">']
    creditos_lines.append(f'<div class="cip-header">{render_paragraph_inner(paragraphs[5])}</div>')
    creditos_lines.append('<div class="cip-box">')
    creditos_lines.append(f'<p class="center"><strong>{render_paragraph_inner(paragraphs[6])}</strong></p>')
    for idx in range(7, 24):
        inner = render_paragraph_inner(paragraphs[idx]).replace('<!--PAGE_BREAK-->', '').strip()
        if inner:
            creditos_lines.append(f'<p class="cip-line">{inner}</p>')
    creditos_lines.append('</div>')

    for idx in range(25, 32):
        inner = render_paragraph_inner(paragraphs[idx]).replace('<!--PAGE_BREAK-->', '').strip()
        if not inner:
            continue
        plain = get_paragraph_plain_text(paragraphs[idx])
        if plain in (
            'Copyright © 2026',
            'Declaração de Autoria e Uso Responsável de Inteligência Artificial',
            'Compromisso Social e Evangelístico'
        ):
            creditos_lines.append(f'<h3 class="legal-heading">{inner}</h3>')
        else:
            creditos_lines.append(f'<p class="no-indent">{inner}</p>')
    creditos_lines.append('</section>')
    creditos_html = wrap_xhtml_document("Ficha Catalográfica e Direitos Autorais", '\n'.join(creditos_lines))

    # 4. NOTA AUTORAL (nota_autoral.xhtml) - P 123 a P 134
    nota_lines = ['<section epub:type="preface">']
    nota_lines.append(f'<h1 id="nota-autoral" class="part-title">{render_paragraph_inner(paragraphs[123])}</h1>')
    for idx in range(124, 135):
        inner = render_paragraph_inner(paragraphs[idx], anchor_map, 'nota_autoral.xhtml').replace('<!--PAGE_BREAK-->', '').strip()
        if inner:
            nota_lines.append(f'<p class="indent">{inner}</p>')
    nota_lines.append('</section>')
    nota_autoral_html = wrap_xhtml_document("Nota Autoral", '\n'.join(nota_lines))

    # 5. PARTES I A V (parte1.xhtml .. parte5.xhtml)
    # Índices de início das Partes:
    # Parte I: 135..240
    # Parte II: 241..310
    # Parte III: 311..361
    # Parte IV: 362..485
    # Parte V: 486..500
    part_specs = [
        ('parte1.xhtml', 'part-1', 135, 241),
        ('parte2.xhtml', 'part-2', 241, 311),
        ('parte3.xhtml', 'part-3', 311, 362),
        ('parte4.xhtml', 'part-4', 362, 486),
        ('parte5.xhtml', 'part-5', 486, 501),
    ]

    toc_structure = []  # Lista de (part_title, part_href, [(sec_title, sec_href), ...])
    part_files_html = {}

    for filename, part_id, start_idx, end_idx in part_specs:
        part_title_plain = get_paragraph_plain_text(paragraphs[start_idx])
        part_title_inner = render_paragraph_inner(paragraphs[start_idx], anchor_map, filename).replace('<!--PAGE_BREAK-->', '').strip()
        lines = [f'<section epub:type="part">']
        lines.append(f'<h1 id="{part_id}" class="part-title">{part_title_inner}</h1>')
        sub_sections = []

        for idx in range(start_idx + 1, end_idx):
            p = paragraphs[idx]
            plain = get_paragraph_plain_text(p)
            if not plain:
                continue
            style_val, jc_val, left_ind, first_ind = get_paragraph_style_and_indent(p)
            inner = render_paragraph_inner(p, anchor_map, filename, fix_p421=(idx == 421)).replace('<!--PAGE_BREAK-->', '').strip()
            if not inner:
                continue

            # Verificar se é cabeçalho de seção (Ttulo2 ou padrão numérico "1. ")
            sec_match = re.match(r'^(\d+)\.\s+', plain)
            if style_val == 'Ttulo2' or sec_match:
                sec_num = sec_match.group(1) if sec_match else f's{idx}'
                sec_id = f'sec-{sec_num}'
                lines.append(f'<h2 id="{sec_id}" class="section-title">{inner}</h2>')
                sub_sections.append((plain, f'{filename}#{sec_id}'))
            else:
                if jc_val == 'center':
                    lines.append(f'<p class="center">{inner}</p>')
                elif left_ind >= 400:
                    lines.append(f'<p class="blockquote">{inner}</p>')
                elif first_ind > 0:
                    lines.append(f'<p class="indent">{inner}</p>')
                else:
                    lines.append(f'<p class="indent">{inner}</p>')

        lines.append('</section>')
        part_files_html[filename] = wrap_xhtml_document(part_title_plain, '\n'.join(lines))
        toc_structure.append((part_title_plain, f'{filename}#{part_id}', sub_sections))

    # 6. ÍNDICE DE VERSÍCULOS MESSIÂNICOS (indice_versiculos.xhtml) - P 501 a P 549
    idx_title_plain = get_paragraph_plain_text(paragraphs[501])
    idx_lines = ['<section epub:type="index">']
    idx_lines.append(f'<h1 id="indice-versiculos" class="part-title">{render_paragraph_inner(paragraphs[501]).replace("<!--PAGE_BREAK-->", "").strip()}</h1>')
    for idx in range(502, 550):
        p = paragraphs[idx]
        plain = get_paragraph_plain_text(p)
        if not plain:
            continue
        inner = render_paragraph_inner(p, anchor_map, 'indice_versiculos.xhtml').replace('<!--PAGE_BREAK-->', '').strip()
        if plain == '- -':
            idx_lines.append(f'<p class="center">{inner}</p>')
        else:
            idx_lines.append(f'<p class="verse-index-item">{inner}</p>')
    idx_lines.append('</section>')
    indice_versiculos_html = wrap_xhtml_document(idx_title_plain, '\n'.join(idx_lines))

    # 7. NOTAS FINAIS (notas_finais.xhtml) - 50 notas de word/endnotes.xml
    en_notes = [
        n for n in en_tree.findall('.//w:endnote', NS)
        if int(n.attrib.get(W_ID, 0)) > 0
    ]
    print(f"Total de Notas Finais processadas: {len(en_notes)}")

    notas_lines = ['<section class="endnotes-section">']
    notas_lines.append('<h1 id="notas-finais" class="part-title">NOTAS FINAIS</h1>')

    for note in en_notes:
        nid = int(note.attrib.get(W_ID))
        back_file = anchor_map.get(nid, 'nota_autoral.xhtml')
        back_href = f'{back_file}#ref{nid}'
        note_paras = note.findall('.//w:p', NS)

        notas_lines.append(f'<div id="fn{nid}" class="endnote-item">')
        non_empty_Rendered = []
        for p_i, np in enumerate(note_paras):
            np_inner = render_paragraph_inner(np, skip_endnote_ref_tag=True).replace('<!--PAGE_BREAK-->', '').strip()
            if np_inner:
                non_empty_Rendered.append((np, np_inner))

        for idx_np, (np, np_inner) in enumerate(non_empty_Rendered):
            is_first = (idx_np == 0)
            is_last = (idx_np == len(non_empty_Rendered) - 1)
            prefix = f'<a href="{back_href}" class="endnote-number" title="Voltar ao texto">[{nid}]</a> ' if is_first else ''
            suffix = f' <a href="{back_href}" class="endnote-backref" title="Voltar ao texto">↩</a>' if is_last else ''
            notas_lines.append(f'  <p class="no-indent">{prefix}{np_inner}{suffix}</p>')

        notas_lines.append('</div>')

    notas_lines.append('</section>')
    notas_finais_html = wrap_xhtml_document("Notas Finais", '\n'.join(notas_lines))

    # 8. BIBLIOGRAFIA (bibliografia.xhtml) e 9. AGRADECIMENTOS (agradecimentos.xhtml)
    # P 553 é BIBLIOGRAFIA, P 555..610 são as 56 entradas (com P 610 contendo <!--PAGE_BREAK-->AGRADECIMENTOS)
    bib_lines = ['<section epub:type="bibliography">']
    bib_lines.append('<h1 id="bibliografia" class="part-title">BIBLIOGRAFIA</h1>')

    agrad_heading = 'AGRADECIMENTOS'
    for idx in range(555, 611):
        p = paragraphs[idx]
        inner = render_paragraph_inner(p, anchor_map, 'bibliografia.xhtml')
        if '<!--PAGE_BREAK-->' in inner:
            parts_pb = inner.split('<!--PAGE_BREAK-->')
            bib_part = parts_pb[0].strip()
            if bib_part:
                bib_lines.append(f'<p class="bib-entry">{bib_part}</p>')
        else:
            clean_inner = inner.strip()
            if clean_inner:
                bib_lines.append(f'<p class="bib-entry">{clean_inner}</p>')

    bib_lines.append('</section>')
    bibliografia_html = wrap_xhtml_document("Bibliografia", '\n'.join(bib_lines))

    # 9. AGRADECIMENTOS (agradecimentos.xhtml) - P 612 a P 625
    agrad_lines = ['<section epub:type="acknowledgments">']
    agrad_lines.append(f'<h1 id="agradecimentos" class="part-title">{agrad_heading}</h1>')
    subheadings_agrad = {
        'A Deus',
        'À Minha Família',
        'Aos Pilares de Vida e Formação',
        'Aos Mentores, Revisores e Parceiros de Ministério',
        'À Igreja e à Liderança Eclesiástica',
        'A Você, Querido Leitor'
    }
    for idx in range(612, 626):
        p = paragraphs[idx]
        plain = get_paragraph_plain_text(p)
        inner = render_paragraph_inner(p, anchor_map, 'agradecimentos.xhtml').replace('<!--PAGE_BREAK-->', '').strip()
        if not inner:
            continue
        if plain in subheadings_agrad:
            agrad_lines.append(f'<h3 class="sub-heading">{inner}</h3>')
        else:
            agrad_lines.append(f'<p class="indent">{inner}</p>')
    agrad_lines.append('</section>')
    agradecimentos_html = wrap_xhtml_document("Agradecimentos", '\n'.join(agrad_lines))

    # 10. PRESENTE ESPECIAL (presente.xhtml) - P 626 a P 638
    pres_lines = ['<section epub:type="afterword">']
    p626_inner = render_paragraph_inner(paragraphs[626]).replace('<!--PAGE_BREAK-->', '').strip()
    p627_inner = render_paragraph_inner(paragraphs[627]).replace('<!--PAGE_BREAK-->', '').strip()
    pres_lines.append(f'<h1 id="presente" class="part-title">{p627_inner}</h1>')
    pres_lines.append(f'<p class="center"><strong>{p626_inner}</strong></p>')
    for idx in range(628, len(paragraphs)):
        p = paragraphs[idx]
        plain = get_paragraph_plain_text(p)
        inner = render_paragraph_inner(p, anchor_map, 'presente.xhtml').replace('<!--PAGE_BREAK-->', '').strip()
        if not inner:
            continue
        if plain.startswith('📚') or plain.startswith('⚠️'):
            pres_lines.append(f'<h3 class="sub-heading">{inner}</h3>')
        elif idx == len(paragraphs) - 1:
            pres_lines.append(f'<p class="center" style="margin-top: 1.5em;"><strong>{inner}</strong></p>')
        else:
            pres_lines.append(f'<p class="no-indent">{inner}</p>')
    pres_lines.append('</section>')
    presente_html = wrap_xhtml_document("Presente Especial", '\n'.join(pres_lines))

    # 11. SUMÁRIO INTERATIVO (sumario.xhtml) E NAVEGAÇÃO NATIVA (nav.xhtml + toc.ncx)
    toc_items_html = []
    toc_items_html.append('<li class="toc-part"><a href="rosto.xhtml">Folha de Rosto</a></li>')
    toc_items_html.append('<li class="toc-part"><a href="creditos.xhtml">Ficha Catalográfica e Direitos Autorais</a></li>')
    toc_items_html.append('<li class="toc-part"><a href="nota_autoral.xhtml#nota-autoral">Nota Autoral</a></li>')

    for part_title, part_href, sub_secs in toc_structure:
        if sub_secs:
            sub_li = '\n'.join(
                [f'      <li class="toc-sec"><a href="{shref}">{html.escape(stitle)}</a></li>' for stitle, shref in sub_secs]
            )
            toc_items_html.append(
                f'<li class="toc-part"><a href="{part_href}">{html.escape(part_title)}</a>\n    <ol class="toc-sublist">\n{sub_li}\n    </ol>\n  </li>'
            )
        else:
            toc_items_html.append(f'<li class="toc-part"><a href="{part_href}">{html.escape(part_title)}</a></li>')

    toc_items_html.append('<li class="toc-part"><a href="indice_versiculos.xhtml#indice-versiculos">Índice de Versículos Messiânicos do Antigo Testamento</a></li>')
    toc_items_html.append('<li class="toc-part"><a href="notas_finais.xhtml#notas-finais">Notas Finais (1–50)</a></li>')
    toc_items_html.append('<li class="toc-part"><a href="bibliografia.xhtml#bibliografia">Bibliografia</a></li>')
    toc_items_html.append('<li class="toc-part"><a href="agradecimentos.xhtml#agradecimentos">Agradecimentos</a></li>')
    toc_items_html.append('<li class="toc-part"><a href="presente.xhtml#presente">Presente Especial</a></li>')

    toc_ol = '<ol class="toc-list">\n  ' + '\n  '.join(toc_items_html) + '\n</ol>'

    sumario_body = f'''<section epub:type="toc">
  <h1 id="sumario" class="part-title">Sumário</h1>
  {toc_ol}
</section>'''
    sumario_html = wrap_xhtml_document("Sumário", sumario_body)

    nav_body = f'''<nav epub:type="toc" id="toc">
  <h1 class="part-title">Sumário</h1>
  {toc_ol}
</nav>
<nav epub:type="landmarks" id="landmarks" hidden="hidden">
  <h2>Guia</h2>
  <ol>
    <li><a epub:type="cover" href="cover.xhtml">Capa</a></li>
    <li><a epub:type="titlepage" href="rosto.xhtml">Folha de Rosto</a></li>
    <li><a epub:type="toc" href="sumario.xhtml">Sumário</a></li>
    <li><a epub:type="bodymatter" href="nota_autoral.xhtml">Início da Leitura</a></li>
    <li><a epub:type="endnotes" href="notas_finais.xhtml">Notas Finais</a></li>
    <li><a epub:type="bibliography" href="bibliografia.xhtml">Bibliografia</a></li>
  </ol>
</nav>'''
    nav_html = wrap_xhtml_document("Navegação", nav_body)

    # 12. CONSTRUIR toc.ncx (EPUB 2 compatibility)
    nav_points = []
    play_order = 1

    def add_nav_point(label, src, children_xml=''):
        nonlocal play_order
        po = play_order
        play_order += 1
        return f'''    <navPoint id="navPoint-{po}" playOrder="{po}">
      <navLabel><text>{html.escape(label)}</text></navLabel>
      <content src="{src}"/>{children_xml}
    </navPoint>'''

    nav_points.append(add_nav_point("Capa", "cover.xhtml"))
    nav_points.append(add_nav_point("Folha de Rosto", "rosto.xhtml"))
    nav_points.append(add_nav_point("Ficha Catalográfica", "creditos.xhtml"))
    nav_points.append(add_nav_point("Sumário", "sumario.xhtml"))
    nav_points.append(add_nav_point("Nota Autoral", "nota_autoral.xhtml#nota-autoral"))

    for part_title, part_href, sub_secs in toc_structure:
        po_parent = play_order
        play_order += 1
        child_pts = []
        for stitle, shref in sub_secs:
            po_c = play_order
            play_order += 1
            child_pts.append(f'''
      <navPoint id="navPoint-{po_c}" playOrder="{po_c}">
        <navLabel><text>{html.escape(stitle)}</text></navLabel>
        <content src="{shref}"/>
      </navPoint>''')
        children_str = ''.join(child_pts)
        nav_points.append(f'''    <navPoint id="navPoint-{po_parent}" playOrder="{po_parent}">
      <navLabel><text>{html.escape(part_title)}</text></navLabel>
      <content src="{part_href}"/>{children_str}
    </navPoint>''')

    nav_points.append(add_nav_point("Índice de Versículos Messiânicos do Antigo Testamento", "indice_versiculos.xhtml#indice-versiculos"))
    nav_points.append(add_nav_point("Notas Finais", "notas_finais.xhtml#notas-finais"))
    nav_points.append(add_nav_point("Bibliografia", "bibliografia.xhtml#bibliografia"))
    nav_points.append(add_nav_point("Agradecimentos", "agradecimentos.xhtml#agradecimentos"))
    nav_points.append(add_nav_point("Presente Especial", "presente.xhtml#presente"))

    toc_ncx = f'''<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="pt-BR">
  <head>
    <meta name="dtb:uid" content="urn:isbn:9786502461709"/>
    <meta name="dtb:depth" content="2"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle>
    <text>O Sermão de Emaús: Você Conhece as Promessas Messiânicas do Antigo Testamento?</text>
  </docTitle>
  <docAuthor>
    <text>Webert T. S. Costa</text>
  </docAuthor>
  <navMap>
{chr(10).join(nav_points)}
  </navMap>
</ncx>
'''

    # 13. CONSTRUIR content.opf
    content_opf = '''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookId" xml:lang="pt-BR">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookId">urn:isbn:9786502461709</dc:identifier>
    <dc:title id="main-title">O Sermão de Emaús: Você Conhece as Promessas Messiânicas do Antigo Testamento?</dc:title>
    <dc:creator id="creator">Webert T. S. Costa</dc:creator>
    <dc:language>pt-BR</dc:language>
    <dc:publisher>Edição do Autor / Spurgeon TV</dc:publisher>
    <dc:date>2026-11-05</dc:date>
    <dc:rights>Copyright © 2026 Webert T. S. Costa. Todos os direitos reservados.</dc:rights>
    <dc:description>Uma reconstrução literária e devocional do ensino de Jesus aos dois discípulos no caminho de Emaús com base em Lucas 24:27, acompanhada de índice de versículos messiânicos e 50 notas exegéticas e teológicas finais.</dc:description>
    <meta property="dcterms:modified">2026-11-05T00:00:00Z</meta>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="css" href="styles/stylesheet.css" media-type="text/css"/>
    <item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>
    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>
    <item id="rosto" href="rosto.xhtml" media-type="application/xhtml+xml"/>
    <item id="creditos" href="creditos.xhtml" media-type="application/xhtml+xml"/>
    <item id="sumario" href="sumario.xhtml" media-type="application/xhtml+xml"/>
    <item id="nota_autoral" href="nota_autoral.xhtml" media-type="application/xhtml+xml"/>
    <item id="parte1" href="parte1.xhtml" media-type="application/xhtml+xml"/>
    <item id="parte2" href="parte2.xhtml" media-type="application/xhtml+xml"/>
    <item id="parte3" href="parte3.xhtml" media-type="application/xhtml+xml"/>
    <item id="parte4" href="parte4.xhtml" media-type="application/xhtml+xml"/>
    <item id="parte5" href="parte5.xhtml" media-type="application/xhtml+xml"/>
    <item id="indice_versiculos" href="indice_versiculos.xhtml" media-type="application/xhtml+xml"/>
    <item id="notas_finais" href="notas_finais.xhtml" media-type="application/xhtml+xml"/>
    <item id="bibliografia" href="bibliografia.xhtml" media-type="application/xhtml+xml"/>
    <item id="agradecimentos" href="agradecimentos.xhtml" media-type="application/xhtml+xml"/>
    <item id="presente" href="presente.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="cover"/>
    <itemref idref="rosto"/>
    <itemref idref="creditos"/>
    <itemref idref="sumario"/>
    <itemref idref="nota_autoral"/>
    <itemref idref="parte1"/>
    <itemref idref="parte2"/>
    <itemref idref="parte3"/>
    <itemref idref="parte4"/>
    <itemref idref="parte5"/>
    <itemref idref="indice_versiculos"/>
    <itemref idref="notas_finais"/>
    <itemref idref="bibliografia"/>
    <itemref idref="agradecimentos"/>
    <itemref idref="presente"/>
  </spine>
  <guide>
    <reference type="cover" title="Capa" href="cover.xhtml"/>
    <reference type="title-page" title="Folha de Rosto" href="rosto.xhtml"/>
    <reference type="toc" title="Sumário" href="sumario.xhtml"/>
    <reference type="text" title="Início" href="nota_autoral.xhtml"/>
    <reference type="notes" title="Notas Finais" href="notas_finais.xhtml"/>
    <reference type="bibliography" title="Bibliografia" href="bibliografia.xhtml"/>
  </guide>
</package>
'''

    container_xml = '''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
'''

    # 14. EMPACOTAR ARQUIVO EPUB
    os.makedirs(os.path.dirname(TARGET_EPUB), exist_ok=True)
    with zipfile.ZipFile(TARGET_EPUB, 'w') as zf:
        # Regra OCF EPUB: mimetype deve ser o primeiro arquivo e SEM compressão
        zf.writestr('mimetype', b'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        # META-INF
        zf.writestr('META-INF/container.xml', container_xml.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

        # OEBPS/content.opf, nav.xhtml, toc.ncx, CSS
        zf.writestr('OEBPS/content.opf', content_opf.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/nav.xhtml', nav_html.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/toc.ncx', toc_ncx.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr('OEBPS/styles/stylesheet.css', STYLESHEET_CSS.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

        # Imagem de Capa
        with open(COVER_JPG, 'rb') as img_f:
            zf.writestr('OEBPS/images/cover.jpg', img_f.read(), compress_type=zipfile.ZIP_DEFLATED)

        # Capítulos XHTML
        xhtml_files = {
            'cover.xhtml': cover_html,
            'rosto.xhtml': rosto_html,
            'creditos.xhtml': creditos_html,
            'sumario.xhtml': sumario_html,
            'nota_autoral.xhtml': nota_autoral_html,
            'parte1.xhtml': part_files_html['parte1.xhtml'],
            'parte2.xhtml': part_files_html['parte2.xhtml'],
            'parte3.xhtml': part_files_html['parte3.xhtml'],
            'parte4.xhtml': part_files_html['parte4.xhtml'],
            'parte5.xhtml': part_files_html['parte5.xhtml'],
            'indice_versiculos.xhtml': indice_versiculos_html,
            'notas_finais.xhtml': notas_finais_html,
            'bibliografia.xhtml': bibliografia_html,
            'agradecimentos.xhtml': agradecimentos_html,
            'presente.xhtml': presente_html,
        }
        for fname, fcontent in xhtml_files.items():
            zf.writestr(f'OEBPS/{fname}', fcontent.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

    size_kb = os.path.getsize(TARGET_EPUB) / 1024
    print(f"[OK] EPUB 3.0 gerado com sucesso: {TARGET_EPUB} ({size_kb:.2f} KB)")
    print(f"[OK] Âncoras de notas mapeadas no corpo: {len(anchor_map)} de 50")


if __name__ == '__main__':
    build_epub()

