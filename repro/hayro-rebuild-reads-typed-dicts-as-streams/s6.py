# n annotation dictionaries and no stream, with a startxref that points nowhere, so the table is rebuilt.
import sys
n = int(sys.argv[2])
out = bytearray(b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>\nendobj\n")
for i in range(n):
    out += b"%d 0 obj\n<< /Type /Annot /Subtype /Text /Rect [0 0 1 1] >>\nendobj\n" % (4 + i)
out += b"trailer\n<< /Root 1 0 R >>\nstartxref\n999999999\n%%EOF\n"
open(sys.argv[1], "wb").write(out)
