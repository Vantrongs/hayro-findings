# One object holding n unterminated `<< /A (`, with a startxref that points nowhere, so the table is rebuilt.
import sys
n = int(sys.argv[2])
out = bytearray(b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
                b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
                b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>\nendobj\n")
out += b"4 0 obj\n" + b"<< /A ( " * n + b"\nendobj\n"
out += b"trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n999999999\n%%EOF\n"
open(sys.argv[1], "wb").write(out)
