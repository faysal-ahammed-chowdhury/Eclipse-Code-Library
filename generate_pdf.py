#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess

code_dir = "code"

def clean_name(name):
    """
    Remove ordering prefix like 01-, 02-, ..., 99- from folder/file names
    """
    parts = name.split('-', 1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1]  # return the part after the prefix
    return name

def get_sections():
    sections = []
    for root, dirs, files in os.walk(code_dir):
        dirs.sort()   # sort subfolders alphabetically (keeps 01-, 02- ordering)
        files.sort()  # sort files alphabetically
        subsections = []
        section_name = os.path.basename(root)
        sections.append((section_name, subsections))
        for file_name in files:
            if file_name.startswith('.'):
                continue  # skip hidden files
            subsection_name = os.path.splitext(file_name)[0]
            relative_path = os.path.join(root, file_name)

            # Count number of lines
            try:
                with open(relative_path, 'r', encoding='utf-8', errors='ignore') as f:
                    number_of_lines = sum(1 for _ in f)
            except Exception:
                number_of_lines = 0

            subsections.append((relative_path, subsection_name, number_of_lines))
    return sections[1:]  # skip the root folder itself

def get_style(filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['c', 'cc', 'cpp']:
        return 'c++'
    elif ext == 'java':
        return 'java'
    elif ext == 'py':
        return 'python'
    else:
        return 'text'

def texify(s):
    # Escape LaTeX special characters
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s

def get_tex(sections):
    tex = ''
    for section_name, subsections in sections:
        clean_section = clean_name(section_name)
        tex += f'\\section{{{texify(clean_section)}}}\n'
        for relative_path, subsection_name, number_of_lines in subsections:
            clean_subsection = clean_name(subsection_name)
            tex += f'\\subsection{{\\small {texify(clean_subsection)}  \\scriptsize [{number_of_lines} lines]}}\n'
            file_path = Path(relative_path).as_posix()  # Linux-style path
            tex += f'\\inputminted{{{get_style(relative_path)}}}{{{file_path}}}\n'
        tex += '\n'
    return tex

if __name__ == "__main__":
    sections = get_sections()
    tex = get_tex(sections)

    with open('contents.tex', 'w', encoding='utf-8') as f:
        f.write(tex)
    
    # Compile LaTeX
    subprocess.call(["latexmk", "-pdf", "-shell-escape", "-cd", "notebook.tex"])