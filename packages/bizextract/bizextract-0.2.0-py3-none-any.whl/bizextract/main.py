from argparse import ArgumentParser
from . import parse_reports, print_table, write_table
from pathlib import Path


def main():
    parser = ArgumentParser('bizextract - a tool to extract business data from PDF reports.')
    parser.add_argument('--pattern', help='A file name pattern to limit the files parsed by the tool.')
    parser.add_argument('output', help='The output path (or file) to write the results. Content will be a CSV file.')

    args = parser.parse_args()
    analysis = parse_reports(args.pattern)
    print_table(analysis)

    outpath = Path(args.output)
    if outpath.is_dir():
        outpath = outpath.joinpath('out.csv')
    write_table(analysis, outpath)
