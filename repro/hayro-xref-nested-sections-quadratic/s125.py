# n xref sections chained by /Prev, each inside a string of the trailer before it,
# with a pad of `a` bytes in the innermost string.
import sys
n, pad = int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 1 << 20
out = bytearray(b"%PDF-1.7\n"); offs = []
for i, o in enumerate([b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
                       b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>"], 1):
    offs.append(len(out)); out += b"%d 0 obj\n%s\nendobj\n" % (i, o)
table = b"xref\n0 4\n0000000000 65535 f \n" + b"".join(b"%010d 00000 n \n" % o for o in offs)
first = len(out)
for i in range(n):
    out += table + b"trailer\n<< /Size 4 /Root 1 0 R "
    if i + 1 < n:
        prev = len(out) + len(b"/Prev 0000000000 /S (")
        out += b"/Prev %010d /S (" % prev
    else:
        out += b"/S ("
out += b"a" * pad + b") >>\n" * n
out += b"startxref\n%d\n%%%%EOF\n" % first
open(sys.argv[1], "wb").write(out)
