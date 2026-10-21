# Writes names-<kind>-<n>.pdf: a one-page file whose catalog holds n more keys of
# 16 bytes. With "colliding", each name's first 8 bytes are rustc-hash's SEED1 in
# little-endian, so hash_bytes multiplies by zero and every name hashes alike.
import struct, sys

kind, n = sys.argv[1], int(sys.argv[2])
prefix = struct.pack("<Q", 0x243F6A8885A308D3) if kind == "colliding" else b"Key00000"
keys = b"".join(b" /" + prefix + b"%08x 1" % i for i in range(n))
objs = [b"<< /Type /Catalog /Pages 2 0 R" + keys + b" >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] >>"]
out = b"%PDF-1.7\n"; offsets = []
for i, o in enumerate(objs, 1):
    offsets.append(len(out)); out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
xref = len(out)
out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1) + b"".join(b"%010d 00000 n \n" % o for o in offsets)
out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
open("names-%s-%d.pdf" % (kind, n), "wb").write(out)
