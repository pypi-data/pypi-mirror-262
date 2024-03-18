import matplotlib.pyplot as plt

from mpl_simple_svg_parser import SVGMplPathIterator

fig, ax = plt.subplots(num=1, clear=True)
ax.set_aspect(1)
fn = "noto-emoji/third_party/region-flags/svg/KR.svg"
fn = "noto-emoji/third_party/region-flags/waved-svg/emoji_u1f1f2_1f1f4.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read(), svg2svg=True, pico=True)
svg_mpl_path_iterator.draw(ax)

x0, y0, x1, y1 = svg_mpl_path_iterator.viewbox
ax.set_xlim(x0, x1)
ax.set_ylim(y0, y1)

k = list(svg_mpl_path_iterator.iter_mpl_path_patch_prop())

import flag_info

info = flag_info._flag_names_from_file_names("KR")



from pathlib import Path
from os import path
import re
root = Path("noto-emoji/third_party/region-flags/waved-svg")

def _flag_char(char_str):
    return chr(ord('A') + int(char_str, 16) - 0x1f1e6)
flag_re = re.compile('emoji_u(1f1[0-9a-f]{2})_(1f1[0-9a-f]{2}).svg')

def _flag_names_from_emoji_file_name(fn):

  m = flag_re.match(path.basename(fn))

  if m:
      flag_short_name = _flag_char(m.group(1)) + _flag_char(m.group(2))

      return flag_short_name

by_codes = {}
for fn in root.glob("*.svg"):
    code = _flag_names_from_emoji_file_name(fn)
    if code:
        by_codes[code] = fn

        svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read(), svg2svg=True,
                                                   pico=True)
        k = list(svg_mpl_path_iterator.iter_mpl_path_patch_prop())
        viewbox = svg_mpl_path_iterator.viewbox
        by_codes[code] = dict(mpl_path_patch_prop=k,
                              viewbox=viewbox,
                              filename=fn)


master_dict = {}
for country, c in by_codes.items():
    # c = by_codes[country]
    vertices = []
    codes = []
    facecolors = []
    for path, prop in c["mpl_path_patch_prop"]:
        if isinstance(prop["fc"], str):
            # We need to support gradients!
            facecolors.append([0, 0, 0, 0])
        else:
            facecolors.append(np.concatenate([prop["fc"], [prop["alpha"]]]))
        vertices.append(path.vertices)
        codes.append(path.codes)

    nn = [len(c) for c in codes]

    master_dict.update({f"{country}_split_index": np.add.accumulate(nn[:-1]),
                        f"{country}_facecolors": np.vstack(facecolors),
                        f"{country}_vertices": np.concatenate(vertices),
                        f"{country}_codes": np.concatenate(codes),
                        },)

np.savez("flags.npz", **master_dict)


master_json = {}
for country, c in by_codes.items():
    master_json[country] = dict(viewbox=c["viewbox"],
                                filename=c["filename"].as_posix())
import json
json.dump(master_json, open("flags.json", "w"), indent=2)
