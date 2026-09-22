#!/usr/bin/env python3
"""extract_pdfs.py

Utility script to extract plain text from one or more PDF files using PyPDF2.

Usage:
    python3 scripts/extract_pdfs.py <pdf_path1> [<pdf_path2> ...]

The script will create a ``.txt`` file next to each PDF with the same basename
(``<pdf_path>.txt``) containing the extracted text. If the output file already
exists it will be overwritten.

The script ensures that ``PyPDF2`` is available; if the import fails it will
attempt to install the package via ``pip`` (user‑wide install). Errors are
reported on ``stderr`` and the script exits with a non‑zero status code.

This helper is intended for repeated use inside the workspace so that future
tasks can reliably obtain PDF contents without relying on external tools such as
``pdftotext`` or ``mutool``.
"""

import sys
import subprocess
from pathlib import Path


def ensure_pypdf2():
    """Import PyPDF2, installing it if necessary.

    Returns the imported module.
    """
    try:
        import PyPDF2  # type: ignore
        return PyPDF2
    except ImportError:
        # Install quietly; use the same python interpreter that runs this script
        print("PyPDF2 not found, installing via pip...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2"])
        import PyPDF2  # type: ignore
        return PyPDF2


def extract_text(pdf_path: Path) -> str:
    """Extract all text from *pdf_path* using PyPDF2.

    Returns the concatenated text of all pages. Empty pages are ignored.
    """
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    reader = PyPDF2.PdfReader(str(pdf_path))
    text_parts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)
    return "\n".join(text_parts)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: extract_pdfs.py <pdf_path> [<pdf_path> ...]", file=sys.stderr)
        sys.exit(1)

    # Ensure PyPDF2 is available before processing files
    ensure_pypdf2()

    for pdf_str in argv:
        pdf_path = Path(pdf_str)
        try:
            txt = extract_text(pdf_path)
            out_path = pdf_path.with_suffix('.txt')
            out_path.write_text(txt, encoding='utf-8')
            print(f"Extracted {pdf_path} -> {out_path} ({len(txt)} chars)")
        except Exception as exc:
            print(f"Error processing {pdf_path}: {exc}", file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()

