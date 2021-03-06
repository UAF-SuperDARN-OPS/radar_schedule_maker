#!/usr/bin/python3
# Minimum requirements are Python 3.6

import argparse
from datetime import date

import schedule_generator
import schedule_parser

today = date.today()

next_month = (today.month + 1) % 12
next_month_year = today.year
if next_month == 1:
    next_month_year = today.year + 1

parser = argparse.ArgumentParser(description='SuperDARN Schedule Maker')
site_group = parser.add_mutually_exclusive_group(required=True)

site_group.add_argument("--site", default=None, type=str,
                        help='Station or site ID for a radar [Example: kod, mcm, sps, adw, ade]')
parser.add_argument("--channel", "-c", default='a', type=str, choices=['a', 'b', 'c', 'd'],
                    help='Channel of the radar [Example: a, b, c, d]')
site_group.add_argument("--sitelist", default=None, type=str, nargs='*',
                        help="List of station ID followed by a period and channel letter [Example: kod.c, kod.d]")
parser.add_argument("-m", "--month", default=next_month, type=int, choices=range(1, 13),
                    help="Enter the numeric value for the month of the schedule")
parser.add_argument("-y", "--year", default=next_month_year, type=int, help="Enter the year of the schedule")
parser.add_argument("-a", "--append", default=False, action='store_true', help="Append the schedule or overwrite file")
parser.add_argument("--header", default=False, action='store_true', help="Print the header at the top of the file")
parser.add_argument("--auto", default=False, action='store_true', help="Removes prompts for automated scripts")
args = parser.parse_args()

print(args)

schedule_file = f"{args.year}{args.month:02}.swg"
schedule_path = f"external/schedules/{args.year}/"

schedule_date = date(args.year, args.month, 1)


def frame_print(framed_str):
    width = len(framed_str)
    print('*' * width)
    print(framed_str)
    print('*' * width)


frame_print(f"Parsing Schedule for {schedule_date.strftime('%B %Y')}")

schedule = schedule_parser.ScheduleParser(schedule_path + schedule_file, args.auto)
schedule.run()

frame_print("Parsed Generic Schedule")
schedule.print_schedule()

correct_schedule = 'n'
if not args.auto:
    correct_schedule = input("Is the parsed schedule correct? Enter 'y' if it is, 'n' if not: ")
else:
    correct_schedule = 'y'

if correct_schedule != 'y':
    quit()

site_list = []

if not args.sitelist:
    site_list = [f"{args.site}.{args.channel}"]
else:
    site_list = args.sitelist

for site in site_list:
    frame_print(f"Generating Schedule for {site}")

    generator = schedule_generator.ScheduleGenerator(site.split('.')[0], site.split('.')[1], schedule.get_schedule())
    generator.run()
    generator.print_schedule()

    correct_schedule = 'n'
    if not args.auto:
        correct_schedule = input("Is the generated schedule correct? Enter 'y' if it is, 'n' if not: ")
    else:
        correct_schedule = 'y'

    if args.append:
        write_mode = 'a'
    else:
        write_mode = 'w'

    if correct_schedule == 'y':
        if not args.auto:
            output_path = f"../schedule_files/{site.split('.')[0]}/{site}.scd"
        else:
            output_path = f"../schedule_archive/{args.year}/{args.month:02}/{args.year}{args.month:02}.{site}.scd"

        with open(output_path, write_mode) as file:
            if args.header:
                generator.generate_header()
                file.write(generator.header)

            file.write("\n")
            file.write(generator.get_schedule())
            file.close()
    else:
        quit()


