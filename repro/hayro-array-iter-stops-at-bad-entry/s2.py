import sys
objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] /Annots [4 0 R 99 0 R 5 0 R] /Contents [6 0 R 99 0 R 7 0 R] >>",
        b"<< /Type /Annot /Subtype /Square /Rect [10 10 20 20] >>",
        b"<< /Type /Annot /Subtype /Square /Rect [30 30 40 40] >>",
        b"<< /Length 9 >>\nstream\n4 w 0 0 m\nendstream",
        b"<< /Length 11 >>\nstream\n100 100 l S\nendstream"]
out = bytearray(b"%PDF-1.7\n"); offs = []
for i, o in enumerate(objs, 1):
    offs.append(len(out)); out += b"%d 0 obj\n%s\nendobj\n" % (i, o)
x = len(out)
out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
out += b"".join(b"%010d 00000 n \n" % o for o in offs)
out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
open(sys.argv[1], "wb").write(out)
