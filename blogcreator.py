#!/usr/bin/env python3.11

import re
import pathlib
import argparse

import markdown
import chatgpt_md_converter

# Initialize arguments
argparser = argparse.ArgumentParser(prog='blogcreator')
argparser.add_argument('filename', help='Markdown file path', type=str)
argparser.add_argument('-o', '--output', help='Output file name', type=str)
args = argparser.parse_args()

# Create an output filepath
output_filename = args.output
if not output_filename:
	output_filename = str(pathlib.Path(args.filename).with_suffix('.html'))
elif pathlib.Path(output_filename).is_dir():
	output_filename = str(pathlib.Path(output_filename) / pathlib.Path(args.filename).with_suffix('.html').name)

# Read input
with open(args.filename, 'r') as input_file:
	md = input_file.read()

# Make convertions from Markdown to HTML
md, code_blocks = chatgpt_md_converter.telegram_formatter.extract_and_convert_code_blocks(md)
md = chatgpt_md_converter.telegram_formatter.reinsert_code_blocks(md, code_blocks)
md = re.sub(r'#(\w+)', r'<p>#\1</p>', md)
html = markdown.markdown(md)

# Write HTML to file
with open(output_filename, 'w') as output_file:
	output_file.write(html)
