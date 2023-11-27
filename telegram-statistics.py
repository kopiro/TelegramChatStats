#! /usr/bin/python3

# _*_ coding: utf-8 _*_

"""
@file 		telegram-statistics.py
@author 	Simon Burkhardt - github.com/mnemocron
@date 		2018.10.01

Post about this code:
https://www.reddit.com/r/LongDistance/comments/9mgcol/oc_chat_statistics_from_telegram_using_python/

Inspiration:
https://www.reddit.com/r/LongDistance/comments/9jud8j/analysis_of_texts_from_a_long_distance/
"""

from __future__ import print_function

import sys
import os
import optparse
import re
import json
import codecs
import numpy as np  # install with pip3
import pandas as pd  # install with pip3
import bokeh  # install with pip3
from pprint import pprint
from collections import Counter
from datetime import datetime
from datetime import timedelta

from _message_numerics import _message_numerics
from _message_graphs import _message_graphs

parser = optparse.OptionParser("telegram-stats")
parser.add_option(
    "-i", "--input-file", dest="indir", type="string", help="chat history file"
)
parser.add_option("-n", "--name", dest="name", type="string", help="name of the person")
parser.add_option("-c", "--id", dest="id", type="string", help="chat id of the person")
parser.add_option(
    "-d",
    "--date-max",
    dest="date",
    type="string",
    help="only count messages after date [YYYY-MM-DD]",
)
parser.add_option(
    "-w",
    "--word-list",
    dest="words",
    type="string",
    help='count occurrences of words -w "John;Vacation"',
)
(opts, args) = parser.parse_args()

# Writes a dict in json format to a file
def dump_to_json_file(conv_path, filename, data):
    with open("__generated__/" + conv_path + "/" + filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=4, sort_keys=True)


# writes data utf-8 encoded to a file
# important for emojis
def dump_to_unicode_file(conv_path, filename, data):
    fh = codecs.open("__generated__/" + conv_path + "/" + filename, "w", "utf-8")
    fh.write(data)
    fh.close()


# writes a dict to a csv format
def dump_dict_to_csv_file(conv_path, filename, dict):
    (
        pd.DataFrame.from_dict(data=dict, orient="index").to_csv(
            "__generated__/" + conv_path + "/" + filename, header=False, sep=";"
        )
    )


def load_file_to_raw(path):
    try:
        with open(path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
        return data
    except IOError:
        print("Error: could not open the file")
        exit(-1)


def select_chat_from_name(data, name):
    try:
        for chat in data["chats"]["list"]:
            if "name" in chat:
                if name == chat["name"]:
                    return chat
        print("Error: invalid chat name: " + name)
        exit(-1)
    except KeyError:
        print("Error: wrong file format (name not found)")


def select_chat_from_id(data, id):
    id = str(id)
    try:
        for chat in data["chats"]["list"]:
            if "id" in chat:
                if id == str(chat["id"]):
                    return chat
    except KeyError:
        print("Error: wrong file format (keys not found)")


def dump_text_results(conv_path, metrics):
    result = ""
    result += "\n" + ("[name: " + metrics["A"]["name"] + "]")
    result += "\n" + ("total message count:     \t" + str(metrics["A"]["total_messages"]))
    result += "\n" + ("total word count:        \t" + str(metrics["A"]["total_words"]))
    result += "\n" + ("total character count:   \t" + str(metrics["A"]["total_chars"]))
    result += "\n" + ("average word count:      \t" + str(metrics["A"]["avg_words"]))
    result += "\n" + ("total unique words:      \t" + str(metrics["A"]["unique_words"]))
    result += "\n" + ("average character count: \t" + str(metrics["A"]["avg_chars"]))

    if "urls" in metrics["A"]:
        result += "\n" + ("used markdown in:        \t" + str(metrics["A"]["urls"]) + " messages")
        result += "\n" + ("total urls in messages:  \t" + str(metrics["A"]["urls"]))
    if "photo" in metrics["A"]:
        result += "\n" + ("total photos:            \t" + str(metrics["A"]["photo"]))
    for key in metrics["A"]["media"]:
        result += "\n" + ("total " + str(key) + " count: \t\t" + str(metrics["A"]["media"][key]))

    result += "\n" + ("")
    result += "\n" + ("[name: " + metrics["B"]["name"] + "]")
    result += "\n" + ("total message count:     \t" + str(metrics["B"]["total_messages"]))
    result += "\n" + ("total word count:        \t" + str(metrics["B"]["total_words"]))
    result += "\n" + ("total character count:   \t" + str(metrics["B"]["total_chars"]))
    result += "\n" + ("average word count:      \t" + str(metrics["B"]["avg_words"]))
    result += "\n" + ("total unique words:      \t" + str(metrics["B"]["unique_words"]))
    result += "\n" + ("average character count: \t" + str(metrics["B"]["avg_chars"]))
    if "urls" in metrics["B"]:
        result += "\n" + ("used markdown in:        \t" + str(metrics["B"]["urls"]) + " messages")
        result += "\n" + ("total urls in messages:  \t" + str(metrics["B"]["urls"]))
    if "photo" in metrics["B"]:
        result += "\n" + ("total photos:            \t" + str(metrics["B"]["photo"]))
    for key in metrics["B"]["media"]:
        result += "\n" + ("total " + str(key) + " count: \t\t" + str(metrics["B"]["media"][key]))

    result += "\n" + ("")
    result += "\n" + ("[ combined stats ]")
    result += "\n" + ("total message count:     \t" + str(metrics["total"]))

    dump_to_unicode_file(conv_path, "text_results.txt", result)


def calculate_metrics(conv_path, chat_data, date_filter):
    metrics = _message_numerics(chat_data, date_filter)
    dump_to_json_file(conv_path, "raw_metrics.json", metrics)

    LIMIT = 5
    
    # Emojis
    ustr = "" + metrics["A"]["name"] + "\n"
    for e in metrics["A"]["emojilist"][:LIMIT]:
        ustr += str(e[0]) + " : " + str(e[1]) + "\n"
    ustr += metrics["B"]["name"] + "\n"
    for e in metrics["B"]["emojilist"][:LIMIT]:
        ustr += str(e[0]) + " : " + str(e[1]) + "\n"
    dump_to_unicode_file(conv_path, "emojis.txt", ustr)

    # Wordlists
    ustr = "" + metrics["A"]["name"] + "\n"
    for e in metrics["A"]["wordlist"][:LIMIT]:
        ustr += str(e[0]) + " : " + str(e[1]) + "\n"
    ustr += metrics["B"]["name"] + "\n"
    for e in metrics["B"]["wordlist"][:LIMIT]:
        ustr += str(e[0]) + " : " + str(e[1]) + "\n"
    dump_to_unicode_file(conv_path, "wordlist.txt", ustr)

    # Big wordlists
    ustr = "" + metrics["A"]["name"] + "\n"
    count = 0
    for e in metrics["A"]["wordlist"]:
        if len(e[1]) >= 5:
            ustr += str(e[0]) + " : " + str(e[1]) + "\n"
            count += 1
        if count >= LIMIT:
            break
    ustr += metrics["B"]["name"] + "\n"
    count = 0
    for e in metrics["B"]["wordlist"]:
        if len(e[1]) >= 5:
            ustr += str(e[0]) + " : " + str(e[1]) + "\n"
            count += 1
        if count >= LIMIT:
            break
    dump_to_unicode_file(conv_path, "bigwordlist.txt", ustr)

    return metrics


def calculate_graphs(conv_path, chat_data, date_filter, wordlist):
    return _message_graphs(conv_path, chat_data, date_filter, wordlist)


# https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        print("Incorrect date format, should be YYYY-MM-DD")
        exit(-1)


def print_available_names(raw_data):
    print("")
    print("available chat names:")
    for chat in raw_data["chats"]["list"]:
        if "name" in chat:
            name = chat["name"]
            if name is not None:
                if len(name) > 13:
                    name = name[:11] + "..."
                if len(name) < 7:
                    name = name + "\t"
            else:
                name = "unknown"
            print(name + " \t" + str(chat["id"]) + " \t(" + chat["type"] + ")")


### MAIN
def main():
    if opts.indir is None:
        parser.print_help()
        exit(0)

    date_filter = "1970-01-01"
    if opts.date is not None:
        validate_date(opts.date)
        date_filter = opts.date

    print("importing raw data...")
    raw_data = load_file_to_raw(opts.indir)

    if "chats" in raw_data:
        print("input data is full chat export")
        if opts.id is None and opts.name is None:
            print("Error: argument <name> not specified.")
            print("I do now know which chat to analyze.")
            print("Available chats are:")
            print_available_names(raw_data)
            exit(0)
        if opts.id is not None:
            chat_data = select_chat_from_id(raw_data, opts.id)
        elif opts.name is not None:
            chat_data = select_chat_from_name(raw_data, opts.name)
    else:
        print("input data is a single chat export")
        chat_data = raw_data

    conv_path = chat_data["name"] + "_" + str(chat_data["id"])
    
    # Create directory
    if not os.path.exists("__generated__/" + conv_path):
        os.makedirs("__generated__/" + conv_path)

    wordlist = ""
    if opts.words is not None:
        wordlist = opts.words.lower().split(";")

    print("calculating metrics...")
    metrics = calculate_metrics(conv_path, chat_data, date_filter)

    print("generating graphs...")
    raw = calculate_graphs(conv_path, chat_data, date_filter, wordlist)
    dump_dict_to_csv_file(conv_path, 
        "raw_weekdays_person.csv", raw["A"]["hourofday"]
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_weekdays_person.csv", raw["B"]["hourofday"]
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_months_person.csv", raw["A"]["months"]
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_months_person.csv", raw["B"]["months"]
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_months_chars_person.csv", raw["A"]["months_chars"]
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_months_chars_person.csv", raw["B"]["months_chars"]
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_pictures_person.csv",
        raw["A"]["monthly_pictures"],
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_pictures_person.csv",
        raw["B"]["monthly_pictures"],
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_calls_person.csv",
        raw["A"]["monthly_calls"],
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_calls_person.csv",
        raw["B"]["monthly_calls"],
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_call_duration_person.csv",
        raw["A"]["monthly_call_duration"],
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_call_duration_person.csv",
        raw["B"]["monthly_call_duration"],
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_time_to_reply_person.csv",
        raw["A"]["monthly_time_to_reply"],
    )
    dump_dict_to_csv_file(conv_path, 
        "raw_monthly_time_to_reply_person.csv",
        raw["B"]["monthly_time_to_reply"],
    )

    dump_text_results(conv_path, metrics)
    
    print("done")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print("Aborted by KeyboardInterrupt")
        exit(0)
