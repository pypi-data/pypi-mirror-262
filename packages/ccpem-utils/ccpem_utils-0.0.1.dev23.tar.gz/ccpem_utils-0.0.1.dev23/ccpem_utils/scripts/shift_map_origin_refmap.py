#
#     Copyright (C) 2019 CCP-EM
#
#     This code is distributed under the terms and conditions of the
#     CCP-EM Program Suite Licence Agreement as a CCP-EM Application.
#     A copy of the CCP-EM licence can be obtained by writing to the
#     CCP-EM Secretary, RAL Laboratory, Harwell, OX11 0FA, UK.


import argparse
from ccpem_utils.map.mrcfile_utils import get_mapobjhandle, write_newmapobj
from ccpem_utils.other.utils import compare_tuple
from pathlib import Path
import os


def parse_args():
    parser = argparse.ArgumentParser(
        description="move map based on non-zero reference map origin or input origin"
    )
    parser.add_argument(
        "-m",
        "--map",
        required=True,
        help="Input map (MRC)",
    )
    parser.add_argument(
        "-refm",
        "--refmap",
        required=False,
        help="Input reference map (MRC) whose origin will be used to shift input map",
    )
    parser.add_argument(
        "-ox",
        "--ox",
        default=0,
        type=float,
        help="Map origin coordinate along X",
    )
    parser.add_argument(
        "-oy",
        "--oy",
        default=0,
        type=float,
        help="Map origin coordinate along Y",
    )
    parser.add_argument(
        "-oz",
        "--oz",
        default=0,
        type=float,
        help="Map origin coordinate along Z",
    )
    parser.add_argument(
        "-odir",
        "--odir",
        required=False,
        default=None,
        help="Output directory",
    )
    parser.add_argument(
        "-ofile",
        "--ofile",
        required=False,
        default=None,
        help="Shifted map filename",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.ofile:
        shifted_map = args.ofile
    else:
        shifted_map = os.path.splitext(os.path.basename(args.map))[0] + "_shifted.mrc"
    if args.odir:
        shifted_map = os.path.join(args.odir, shifted_map)
    # Find map origin
    wrapped_mapobj = get_mapobjhandle(args.map)
    if args.refmap:
        wrapped_refmapobj = get_mapobjhandle(args.refmap)
        if wrapped_mapobj.check_origin_zero:
            wrapped_mapobj.fix_origin()
        print("Shifting to reference map origin {}".format(wrapped_refmapobj.origin))
        # same origin? just create a symlink
        if compare_tuple(wrapped_mapobj.origin, wrapped_refmapobj.origin):
            Path(shifted_map).symlink_to(args.map)
        wrapped_mapobj.shift_origin(wrapped_refmapobj.origin)
    else:
        print("Shifting the origin to {}".format((args.ox, args.oy, args.oz)))
        wrapped_mapobj.shift_origin((args.ox, args.oy, args.oz))

    write_newmapobj(wrapped_mapobj, shifted_map)


if __name__ == "__main__":
    main()
