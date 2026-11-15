"""Make vendor/outline.json: the land outline the local routes map draws under its markers.

Why: a published artifact blocks remote images, so the map's street tiles cannot load there. The outline is a
local file, so the map still shows where each area is. Run: python3 -I tools/make_outline.py <countries-50m.json>
Source: world-atlas 2.0.2 (npm), countries-50m.json, which is Natural Earth 1:50m admin-0 (public domain).
Keeps the United Kingdom (826), Ireland (372) and the Isle of Man (833), rounded to 3 decimal places.
"""
import json, sys, os

KEEP = {"826": "United Kingdom", "372": "Ireland", "833": "Isle of Man"}

def decode(topo):
    sx, sy = topo["transform"]["scale"]; tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0; pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append([round(x * sx + tx, 3), round(y * sy + ty, 3)])
        arcs.append(pts)
    def ring(ix):
        out = []
        for i in ix:
            pts = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(pts if not out else pts[1:])
        return out
    return ring

def main(path, out):
    topo = json.load(open(path, encoding="utf-8")); ring = decode(topo)
    feats = []
    for g in topo["objects"]["countries"]["geometries"]:
        gid = str(g.get("id"))
        if gid not in KEEP: continue
        polys = g["arcs"] if g["type"] == "MultiPolygon" else [g["arcs"]]
        coords = [[ring(r) for r in p] for p in polys]
        feats.append({"type": "Feature", "properties": {"name": KEEP[gid], "id": gid},
                      "geometry": {"type": "MultiPolygon", "coordinates": coords}})
    missing = set(KEEP) - {f["properties"]["id"] for f in feats}
    if missing: sys.exit(f"outline: source has no geometry for {sorted(missing)}")
    doc = {"type": "FeatureCollection", "source": "Natural Earth 1:50m admin-0 via world-atlas 2.0.2 (public domain)", "features": feats}
    open(out, "w", encoding="utf-8").write(json.dumps(doc, separators=(",", ":")))
    print(out, os.path.getsize(out), "bytes,", len(feats), "features")

if __name__ == "__main__":
    R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1], os.path.join(R, "vendor", "outline.json"))
