import argparse
import logging
import pathlib

import zonefilegen
import zonefilegen.parsing
import zonefilegen.generation


def generate():
    parser = argparse.ArgumentParser(description='Generate DNS zone files.')
    parser.add_argument('input_file', type=pathlib.Path, help='Input file in TOML format')
    parser.add_argument('output_dir', type=pathlib.Path, help='Output directory where generated zone files will be placed')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--version', action='version', version=zonefilegen.__version__)
    args = parser.parse_args()

    log_level = logging.WARNING
    if args.verbose > 1:
        log_level = logging.DEBUG
    elif args.verbose > 0:
        log_level = logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    (fwd_zone, reverse_zones, soa_dict, input_digest) = zonefilegen.parsing.parse_toml_file(args.input_file)

    for zone in reverse_zones:
        zonefilegen.generation.gen_zone(zone, args.output_dir, soa_dict, input_digest)

    zonefilegen.generation.gen_zone(fwd_zone, args.output_dir, soa_dict, input_digest)
