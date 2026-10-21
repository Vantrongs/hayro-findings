# Object stream 4 holds objects 3 and 5 at indices 0 and 1; the xref stream lists both at index 1.
import sys
members = [b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] >>",
           b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 111 111] >>"]
header = b"3 0 5 %d " % (len(members[0]) + 1)
body = header + members[0] + b"\n" + members[1]
out = bytearray(b"%PDF-1.7\n"); offs = {}
def obj(num, data):
    offs[num] = len(out); out.extend(b"%d 0 obj\n%s\nendobj\n" % (num, data))
obj(1, b"<< /Type /Catalog /Pages 2 0 R >>")
obj(2, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
obj(4, b"<< /Type /ObjStm /N 2 /First %d /Length %d >>\nstream\n%s\nendstream" % (len(header), len(body), body))
offs[6] = len(out)
rows = [(0, 0, 255), (1, offs[1], 0), (1, offs[2], 0), (2, 4, 1), (1, offs[4], 0), (2, 4, 1), (1, offs[6], 0)]
hexdata = b" ".join(b"%02X%04X%02X" % r for r in rows) + b">"
out += b"6 0 obj\n<< /Type /XRef /Size 7 /W [1 2 1] /Root 1 0 R /Filter /ASCIIHexDecode /Length %d >>\nstream\n%s\nendstream\nendobj\n" % (len(hexdata), hexdata)
out += b"startxref\n%d\n%%%%EOF\n" % offs[6]
open(sys.argv[1], "wb").write(out)
