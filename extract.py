import zipfile, xml.etree.ElementTree as ET
import glob
import re

def extract_docx(path):
    z = zipfile.ZipFile(path)
    doc = ET.fromstring(z.read('word/document.xml'))
    return ''.join(node.text for node in doc.iter() if node.text)

def extract_pptx(path):
    z = zipfile.ZipFile(path)
    text = []
    # slides are in ppt/slides/slideX.xml
    for info in z.infolist():
        if info.filename.startswith('ppt/slides/') and info.filename.endswith('.xml'):
            doc = ET.fromstring(z.read(info.filename))
            for node in doc.iter():
                if node.text:
                    text.append(node.text)
    return ' '.join(text)

def extract_rtf(path):
    with open(path, 'r', encoding='latin1') as f:
        text = f.read()
    chars = [chr(int(m.group(1))) for m in re.finditer(r'\\u(-?\d+)', text)]
    return ''.join(chars)

for f in glob.glob('*.*'):
    if f.endswith('.docx'):
        with open(f + '.txt', 'w', encoding='utf-8') as out:
            out.write(extract_docx(f))
    elif f.endswith('.pptx'):
        with open(f + '.txt', 'w', encoding='utf-8') as out:
            out.write(extract_pptx(f))
    elif f.endswith('.rtf'):
        with open(f + '.txt', 'w', encoding='utf-8') as out:
            out.write(extract_rtf(f))
