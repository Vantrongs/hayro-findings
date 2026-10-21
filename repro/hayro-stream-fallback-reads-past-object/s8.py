# n pages whose content streams say /Length 1 and have no endstream.
import sys
n = int(sys.argv[2])
kids = b" ".join(b"%d 0 R" % (3 + 2 * i) for i in range(n))
objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, n)]
for i in range(n):
    objs.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] /Contents %d 0 R >>" % (4 + 2 * i))
    objs.append(b"<< /Length 1 >>\nstream\n0 0 m 100 100 l S")
out = bytearray(b"%PDF-1.7\n"); offs = []
for i, o in enumerate(objs, 1):
    offs.append(len(out)); out += b"%d 0 obj\n%s\nendobj\n" % (i, o)
x = len(out)
out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
out += b"".join(b"%010d 00000 n \n" % o for o in offs)
out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
open(sys.argv[1], "wb").write(out)
