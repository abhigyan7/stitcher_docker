#!/usr/bin/env python3
import argparse
import os
import glob
import re
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser(
    prog = 'panorama.py',
    description = """Create a panorama from a panotools template. Stores intermediaries
    in a directory in /tmp and cleans up before exiting."""
)

parser.add_argument('input_images', metavar='N', type=str, nargs='+',
                    help='images to stitch into a panorama')
parser.add_argument('--template', type=str,
                    help='panotools project file (.pto) to use as the template')
parser.add_argument('--output', type=str,
                    help='output tiff file name')
parser.add_argument('--compression', type=str,
                    help='compression level for output. 0 to 100 for jpeg output and deflate/jpeg/lzw/none/packbits for tiff')
args = parser.parse_args()

template_filename = args.template
input_image_filenames = args.input_images

with tempfile.TemporaryDirectory() as tmpdirname:

    print(f"Working in directory {tmpdirname}", file=sys.stderr)

    # Quote every filename before passing them on to nona
    nona_input_filenames = [f'{w}' for w in input_image_filenames]
    nona_arguments = [f'-o', f'{tmpdirname}/out', '-m', 'TIFF_m', f'{template_filename}']
    nona_proc = subprocess.run(['nona', *nona_arguments, *nona_input_filenames])

    if (nona_proc.returncode != 0):
        print("Nona failed, error: ", nona_proc.stderr, file=sys.stderr)
        print("Exiting...")
        exit(-1)
    print("Remapped inputs, stitching with enblend...", file=sys.stderr)

    # Glob the output files from nona and quote them before enblend
    enblend_input_files = glob.glob(f'{tmpdirname}/out*.tif')
    enblend_arguments = [f'-o',  f'{args.output}', '--pre-assemble']
    if args.compression is not None:
        enblend_arguments.append(f'--compression={args.compression}')
    enblend_proc = subprocess.run(['enblend', *enblend_arguments, *enblend_input_files])
    if (nona_proc.returncode != 0):
        print("Enblend failed, error: ", enblend_proc.stderr, file=sys.stderr)
        print("Exiting...")
        exit(-1)
    print("Stitched, all good.", file=sys.stderr)
