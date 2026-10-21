# Writes short-last-row.pdf: a page whose content stream is Flate-compressed with
# /Predictor 12 /Columns 5, its 26 bytes making five whole rows and a last row of one byte.
import zlib

content = b"0 0 1 rg 10 10 50 50 re  f"
rows = b"".join(b"\0" + content[i:i + 5] for i in range(0, len(content), 5))
data = zlib.compress(rows)
objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] /Contents 4 0 R >>",
        b"<< /Filter /FlateDecode /DecodeParms << /Predictor 12 /Columns 5 >> /Length %d >>\nstream\n"
        % len(data) + data + b"\nendstream"]
out = b"%PDF-1.7\n"; offsets = []
for i, o in enumerate(objs, 1):
    offsets.append(len(out)); out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
xref = len(out)
out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1) + b"".join(b"%010d 00000 n \n" % o for o in offsets)
out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
open("short-last-row.pdf", "wb").write(out)
