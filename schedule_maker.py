#!/usr/bin/python3
# Minimum requirements are Python 3.6

import argparse

parser = argparse.ArgumentParser(description='SuperDARN Schedule Maker')
site_group = parser.add_mutually_exclusive_group(required=True)

site_group.add_argument("--site", default=None, type=str,
                        help='Station or site ID for a radar [Example: kod, mcm, sps, adw, ade]')
parser.add_argument("--channel", "-c", default='a', type=str, choices=['a', 'b', 'c', 'd'],
                    help='Channel of the radar [Example: a, b, c, d]')
site_group.add_argument("--sitelist", default=None, type=str, nargs='*',
                        help="List of station ID followed by a period and channel letter [Example: kod.c, kod.d]")
parser.add_argument("-m", "--month", choices=range(1, 13),
                    help="Enter the numeric value for the month of the schedule")
parser.add_argument("-y", "--year", type=int, help="Enter the year of the schedule")

args = parser.parse_args()

print(args.sitelist)