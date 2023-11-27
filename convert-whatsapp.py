#!/usr/bin/python3

# _*_ coding: utf-8 _*_

from __future__ import print_function

import sys
import os
import optparse
import json
import re
from pprint import pprint

parser = optparse.OptionParser("convert-whatsapp.py")
parser.add_option(
    "-i", "--input-file", dest="indir", type="string", help="chat history file"
)
(opts, args) = parser.parse_args()

dateformat = "EU"
dateseprarator = "."

# Writes a dict in json format to a file
def dump_to_json_file(filename, data):
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)


def load_file_to_srting(filename):
    with open(filename, "r") as fh:
        data = fh.read()
    return data


def split_string_to_messages(string):
    messages = []
    for line in string.split("\n["):
        messages.append(line)
    return messages


def to_telegram_format(messages):
    data = {}
    data["chats"] = {}
    data["chats"]["about"] = "This page lists all chats from this export."
    data["chats"]["list"] = []
    data["chats"]["list"].append({})
    data["chats"]["list"][0]["name"] = "unknown"
    data["chats"]["list"][0]["id"] = 1
    data["chats"]["list"][0]["type"] = "personal_chat"
    data["chats"]["list"][0]["messages"] = []

    id = 0
    for message in messages:
        media = False
        msg_split = message.split("]", 1)
        date_time = msg_split[0].replace('[', '')
        date_ = date_time.split(",")[0]
        date_y = int(date_.split("-")[-1])
        date_m = int(date_.split("-")[1])
        date_d = int(date_.split("-")[0])
        time_ = date_time.split(",")[1]
        time_h = time_.split(":")[0]
        time_m = time_.split(":")[1]
        time_s = time_.split(":")[2]
        msg_1_split = msg_split[1].split(":", 1)
        name = msg_1_split[0].strip()
        text = msg_1_split[1].strip()
        if "<medi" in text.lower():
            media = True
        data["chats"]["list"][0]["messages"].append({})
        data["chats"]["list"][0]["messages"][-1]["id"] = id
        data["chats"]["list"][0]["messages"][-1]["type"] = "message"
        data["chats"]["list"][0]["messages"][-1]["date"] = (
            str(date_y).zfill(2)
            + "-"
            + str(date_m).zfill(2)
            + "-"
            + str(date_d).zfill(2)
            + "T"
            + str(time_h).zfill(2)
            + ":"
            + str(time_m).zfill(2)
            + ":"
            + str(time_s).zfill(2)
        )
        data["chats"]["list"][0]["messages"][-1]["edited"] = "1970-01-01T01:00:00"
        data["chats"]["list"][0]["messages"][-1]["from"] = name
        data["chats"]["list"][0]["messages"][-1]["text"] = text
        id += 1
    return data


### MAIN
def main():
    if opts.indir is None:
        parser.print_help()
        exit(0)
    raw = load_file_to_srting(opts.indir)
    messages = split_string_to_messages(raw)
    formatted = to_telegram_format(messages)
    dump_to_json_file("__import__/whatsapp-result.json", formatted)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("Aborted by KeyboardInterrupt")
        exit(0)
