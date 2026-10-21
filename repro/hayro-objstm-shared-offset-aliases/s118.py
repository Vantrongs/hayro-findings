# An object stream whose member table lists objects 5 .. 5+n-1 all at offset 0, where one
# dictionary refers to all n of them; the page uses object 5 as an ExtGState.
import sys
n = int(sys.argv[2])
nums = range(5, 5 + n)
member = b"<< /A [%s] >>" % b" ".join(b"%d 0 R" % k for k in nums)
header = b"".join(b"%d 0 " % k for k in nums)
body = header + member
out = bytearray(b"%PDF-1.7\n"); offs = {}
def obj(num, data):
    offs[num] = len(out); out.extend(b"%d 0 obj\n%s\nendobj\n" % (num, data))
obj(1, b"<< /Type /Catalog /Pages 2 0 R >>")
obj(2, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
obj(3, b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] /Resources << /ExtGState << /G 5 0 R >> >> >>")
obj(4, b"<< /Type /ObjStm /N %d /First %d /Length %d >>\nstream\n%s\nendstream" % (n, len(header), len(body), body))
size = 5 + n + 1
xref_num = size - 1
offs[xref_num] = len(out)
rows = [(0, 0, 0xFFFF), (1, offs[1], 0), (1, offs[2], 0), (1, offs[3], 0), (1, offs[4], 0)]
rows += [(2, 4, i) for i in range(n)] + [(1, offs[xref_num], 0)]
data = b"".join(bytes([t]) + a.to_bytes(4, "big") + b.to_bytes(2, "big") for t, a, b in rows)
out += b"%d 0 obj\n<< /Type /XRef /Size %d /W [1 4 2] /Root 1 0 R /Length %d >>\nstream\n" % (xref_num, size, len(data))
out += data + b"\nendstream\nendobj\nstartxref\n%d\n%%%%EOF\n" % offs[xref_num]
open(sys.argv[1], "wb").write(out)
