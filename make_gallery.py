#!/usr/bin/env python3

"""
AGB: May 2026, with help from ChatGPT
Read a bash script like SM/SM.sh containing simpleFeynman.py commands and mv commands,
then generate an HTML and Markdown table with 3 columns.
The pdf files need to exist before running this. So, for example, you need to run: source SM.sh to get the pdf files.
If the jpg version of the pdf file already exists, it uses that one. So if you need to change it, then re-run the .sh script to produce a new pdf and delete the jpg version.

Each table cell contains:
  - the python3 simpleFeynman.py command
  - the PDF embedded in the page

Usage:
    python3 make_gallery.py input.sh

Output: input.html and input.md (takes the .sh name and converts it to .html and .md)

Requires: convert (ImageMagick) to convert pdf to jpg for display.
"""

import os
import re
import sys
from html import escape
import subprocess


def parse_script(filename):
    """
    Parse the bash script and pair:
      python3 simpleFeynman.py ...
    with:
      mv -f something.pdf finalname.pdf
    """

    entries = []
    current_command = None
    with open(filename, "r") as f:
        for raw_line in f:
            line = raw_line.strip()

            # Skip empty lines
            if not line:
                continue

            # Save the python command
            if line.startswith("python3") and "simpleFeynman.py" in line:
                current_command = line

            # Match mv command
            elif line.startswith("mv") or line.startswith("epstopdf"):
                parts = line.split()
                # Expect: mv -f source.pdf target.pdf or mv source.pdf target.pdf
                if len(parts) >= 3 and current_command:
                    # Last argument is the destination file
                    output_pdf = parts[-1]

                    entries.append({
                        "command": current_command,
                        "pdf": output_pdf
                    })

                    current_command = None

    return entries

def pdf_to_jpg(pdf_file):
    """
    Convert PDF to JPG using convert. If the JPG already exists, skip conversion.
    """
    base = os.path.splitext(pdf_file)[0]
    jpg_file = base + ".jpg"
    # Skip conversion if JPG already exists
    if os.path.exists(jpg_file):
        print(f"Using existing JPG: {jpg_file}")
        return jpg_file
    tmp_prefix = base + "_tmp"

    #cmd = ["pdftoppm","-jpeg","-singlefile","-r", "200",pdf_file,tmp_prefix]
    cmd = ["convert","-density","300","-trim",pdf_file,tmp_prefix+".jpg"]

    try:
        subprocess.run(cmd, check=True)

        generated = tmp_prefix + ".jpg"

        if os.path.exists(generated):
            os.rename(generated, jpg_file)

        return jpg_file

    except subprocess.CalledProcessError:
        print(f"Failed to convert {pdf_file}")
        return None

def make_html(entries, output_html):
    """
    Generate HTML gallery table with 3 columns.
    Each cell contains:
      - the command
      - the JPG image
      - a PDF link
    """

    html = []

    html.append("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Feynman Diagram Gallery</title>

<style>
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    background: #f5f5f5;
}

table {
    width: 100%;
    border-collapse: collapse;
}

td {
    width: 33%;
    vertical-align: top;
    border: 1px solid #ccc;
    padding: 10px;
    background: white;
}

.command {
    font-family: monospace;
    font-size: 12px;
    margin-bottom: 10px;
    white-space: pre-wrap;
    word-break: break-word;
}

iframe {
    width: 100%;
    height: 400px;
    border: none;
}
</style>
</head>

<body>

<h1>Feynman Diagram Gallery</h1>

<table>
<tr>
""")

    for i, entry in enumerate(entries):

        if i > 0 and i % 3 == 0:
            html.append("</tr><tr>")

        command = escape(entry["command"])
        pdf = escape(entry["pdf"])
        jpg = pdf_to_jpg(pdf)

        if jpg is None:
            jpg_html = "<p>Conversion failed</p>"
        else:
            jpg_html = f'<img src="{escape(jpg)}" width="500">'

        cell = f"""
<td>
<div class="command">{command}</div>

{jpg_html}

<p>
<a href="{pdf}">{pdf}</a><br>
</p>

</td>
"""

        html.append(cell)

    html.append("""
</tr>
</table>

</body>
</html>
""")

    with open(output_html, "w") as f:
        f.write("\n".join(html))


def make_markdown(entries, output_md):
    """
    Generate a GitHub-friendly markdown table with 3 columns.

    Each cell contains:
      - the command
      - the JPG image
      - a PDF link
    """

    md = []

    md.append("# Feynman Diagram Gallery\n")

    cols = 3

    # Table header
    md.append("| Diagram | Diagram | Diagram |")
    md.append("|---|---|---|")

    row = []

    for i, entry in enumerate(entries):

        command = entry["command"]

        pdf = entry["pdf"]

        jpg = pdf_to_jpg(pdf)

        if jpg is None:
            image_md = "Conversion failed"
        else:

            image_md = (
                f"<img src=\"{jpg}\" width=\"500\"><br>"
                f"`{command}`<br>"
                f"[PDF]({pdf})"
            )

        row.append(image_md)

        # Complete row
        if len(row) == cols:

            md.append("| " + " | ".join(row) + " |")

            row = []

    # Fill incomplete final row
    if row:

        while len(row) < cols:
            row.append("")

        md.append("| " + " | ".join(row) + " |")

    with open(output_md, "w") as f:
        f.write("\n".join(md))

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("    python3 make_gallery.py path/to/diagrams.sh")
        sys.exit(1)

    input_script = sys.argv[1]

    # Absolute path to bash script
    input_script = os.path.abspath(input_script)

    if not os.path.exists(input_script):
        print(f"File not found: {input_script}")
        sys.exit(1)

    # Directory containing bash script
    script_dir = os.path.dirname(input_script)
    # Base name without extension
    base_name = os.path.splitext(os.path.basename(input_script))[0]
    # Auto-generated outputs
    output_html = os.path.join(script_dir, base_name + ".html")
    output_md = os.path.join(script_dir, base_name + ".md")

    # Change working directory so PDFs/JPGs are found correctly
    os.chdir(script_dir)
    entries = parse_script(input_script)
    if not entries:
        print("No entries found.")
        sys.exit(1)

    make_html(entries, output_html)
    make_markdown(entries, output_md)

    print(f"Wrote HTML gallery: {output_html}")
    print(f"Wrote Markdown gallery: {output_md}")


if __name__ == "__main__":
    main()
