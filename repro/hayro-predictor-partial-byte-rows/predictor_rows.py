# Writes predictor-rows.pdf: objects 3 to 7 are Flate streams of predicted rows.
import zlib

cases = [
    (b"/Predictor 2 /Colors 3 /BitsPerComponent 2 /Columns 1", bytes.fromhex("6c6c6c")),
    (b"/Predictor 2 /Colors 3 /BitsPerComponent 4 /Columns 1", bytes.fromhex("123012301230")),
    (b"/Predictor 2 /Colors 1 /BitsPerComponent 4 /Columns 3", bytes.fromhex("100010001000")),
    (b"/Predictor 2 /BitsPerComponent 1 /Columns 3", bytes.fromhex("808080")),
    (b"/Predictor 12 /Colors 3 /BitsPerComponent 4 /Columns 3", bytes.fromhex("010101010101020101010101")),
]
objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [] /Count 0 >>"]
for parms, rows in cases:
    data = zlib.compress(rows)
    objs.append(b"<< /Filter /FlateDecode /DecodeParms << %s >> /Length %d >>\nstream\n" % (parms, len(data))
                + data + b"\nendstream")
out = b"%PDF-1.7\n"; offsets = []
for i, o in enumerate(objs, 1):
    offsets.append(len(out)); out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
xref = len(out)
out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1) + b"".join(b"%010d 00000 n \n" % o for o in offsets)
out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
open("predictor-rows.pdf", "wb").write(out)
