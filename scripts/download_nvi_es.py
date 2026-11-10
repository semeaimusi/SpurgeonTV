import sys
import urllib.request
import json
import os
import re
import xml.etree.ElementTree as ET

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load canonical book definitions from rvr1960 to ensure identical Spanish naming and abbreviations
with open('public/bibles/rvr1960.json', 'r', encoding='utf-8') as f:
    rvr_books = json.load(f)

url = 'https://raw.githubusercontent.com/Beblia/Holy-Bible-XML-Format/master/SpanishNVIBible.xml'
cache_xml = r'C:\Users\fcout\.gemini\antigravity\brain\3381e767-4461-4bae-afd4-138ff074fbc7\scratch\SpanishNVIBible.xml'
os.makedirs(os.path.dirname(cache_xml), exist_ok=True)
if os.path.exists(cache_xml):
    print("Loading cached SpanishNVIBible.xml from:", cache_xml)
    with open(cache_xml, 'rb') as f:
        xml_bytes = f.read()
else:
    print("Downloading NVI 1999 Classic XML dataset from:", url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        xml_bytes = resp.read()
    with open(cache_xml, 'wb') as f:
        f.write(xml_bytes)

root = ET.fromstring(xml_bytes)
books_xml = root.findall('.//book')
print(f"Total books in SpanishNVIBible.xml: {len(books_xml)}")
assert len(books_xml) == 66, f"Expected 66 books, got {len(books_xml)}"

converted_bible = []

for idx, book_elem in enumerate(books_xml):
    target_meta = rvr_books[idx]
    book_name = target_meta['name']
    abbrev = target_meta['abbrev']
    expected_chapters = len(target_meta['chapters'])

    chapters_xml = book_elem.findall('chapter')
    raw_chapters = []
    for chap_elem in chapters_xml:
        verse_dict = {}
        for v_elem in chap_elem.findall('verse'):
            v_num = int(v_elem.attrib.get('number', 0))
            v_text = ''.join(v_elem.itertext()).strip()
            v_text = re.sub(r'\s+', ' ', v_text)
            if v_num > 0:
                verse_dict[v_num] = v_text
        max_verse = max(verse_dict.keys()) if verse_dict else 0
        chapter_verses = [verse_dict.get(v, '') for v in range(1, max_verse + 1)]
        # Deduplicate consecutive identical chapters (fixes upstream Beblia XML bug where Isaiah 65 is duplicated as ch 65 & 66 and ch 66 is labeled 67)
        if raw_chapters and raw_chapters[-1] == chapter_verses:
            print(f"  Deduplicated identical consecutive chapter in {book_name} (xml chapter number={chap_elem.attrib.get('number')})")
            continue
        raw_chapters.append(chapter_verses)

    assert len(raw_chapters) == expected_chapters, (
        f"Chapter count mismatch in {book_name} (book #{idx+1}): "
        f"got {len(raw_chapters)}, expected {expected_chapters}"
    )
    converted_chapters = raw_chapters

    converted_bible.append({
        'abbrev': abbrev,
        'name': book_name,
        'chapters': converted_chapters
    })

dest_file = 'public/bibles/nvies.json'
with open(dest_file, 'w', encoding='utf-8') as f:
    json.dump(converted_bible, f, ensure_ascii=False)

size_mb = os.path.getsize(dest_file) / (1024 * 1024)
print(f"Successfully converted and saved {dest_file} ({size_mb:.2f} MB)")

print("\n--- Spot-Check Samples (NVI 1999 Clásica) ---")
print("Génesis 1:1-3:")
for i, v in enumerate(converted_bible[0]['chapters'][0][:3], 1):
    print(f"  v{i}: {v}")
print("\nGénesis 2:7:")
print(f"  {converted_bible[0]['chapters'][1][6]}")
print("\nGénesis 3:15:")
print(f"  {converted_bible[0]['chapters'][2][14]}")
print("\nSalmos 1:1:")
print(f"  {converted_bible[18]['chapters'][0][0]}")
print("\nIsaías 65:1:")
print(f"  {converted_bible[22]['chapters'][64][0]}")
print("\nIsaías 66:1:")
print(f"  {converted_bible[22]['chapters'][65][0]}")
print("\nJuan 3:16:")
print(f"  {converted_bible[42]['chapters'][2][15]}")
print("\nRomanos 8:28:")
print(f"  {converted_bible[44]['chapters'][7][27]}")
