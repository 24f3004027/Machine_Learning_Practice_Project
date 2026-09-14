import os
import sys

def create_pdf_report(md_path: str, pdf_path: str):
    """Creates a multi-page valid PDF report from report.md text."""
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    objects = []
    # Catalog
    objects.append(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
    # Pages (Multi-page container)
    objects.append(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R, 4 0 R] /Count 2 >>\nendobj\n')
    # Page 1
    objects.append(b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 7 0 R >>\nendobj\n')
    # Page 2
    objects.append(b'4 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 8 0 R >>\nendobj\n')
    # Fonts
    objects.append(b'5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n')
    objects.append(b'6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n')

    # Build page 1 and page 2 streams
    p1_cmds = ["BT /F2 18 Tf 50 740 Td (IIT Madras MLP Project: Technical Report) Tj ET"]
    p2_cmds = ["BT /F2 18 Tf 50 740 Td (Empirical Validation & Pipeline Results) Tj ET"]

    y1, y2 = 700, 700
    for i, line in enumerate(lines):
        clean_text = line.replace('(', '\\(').replace(')', '\\)').encode('latin-1', 'replace').decode('latin-1')
        is_heading = line.startswith('#')
        font_tag = "/F2 11 Tf" if is_heading else "/F1 9 Tf"
        spacing = 18 if is_heading else 13

        if i < 35:
            p1_cmds.append(f"BT {font_tag} 50 {y1} Td ({clean_text[:85]}) Tj ET")
            y1 -= spacing
        else:
            p2_cmds.append(f"BT {font_tag} 50 {y2} Td ({clean_text[:85]}) Tj ET")
            y2 -= spacing

    st1 = "\n".join(p1_cmds).encode('latin-1')
    st2 = "\n".join(p2_cmds).encode('latin-1')

    objects.append(f"7 0 obj\n<< /Length {len(st1)} >>\nstream\n".encode('latin-1') + st1 + b"\nendstream\nendobj\n")
    objects.append(f"8 0 obj\n<< /Length {len(st2)} >>\nstream\n".encode('latin-1') + st2 + b"\nendstream\nendobj\n")

    with open(pdf_path, 'wb') as f:
        f.write(b"%PDF-1.4\n")
        offsets = [0]
        pos = 8
        for obj in objects:
            offsets.append(pos)
            f.write(obj)
            pos += len(obj)

        xref_pos = pos
        f.write(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode('latin-1'))
        for off in offsets[1:]:
            f.write(f"{off:010d} 00000 n \n".encode('latin-1'))

        f.write(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode('latin-1'))

    print(f"Successfully created {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

if __name__ == "__main__":
    create_pdf_report("report.md", "Technical_Report.pdf")