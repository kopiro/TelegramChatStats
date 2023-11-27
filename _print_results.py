#! /usr/bin/python3

# _*_ coding: utf-8 _*_

"""
@file 		print-results.py
@author 	Simon Burkhardt - github.com/mnemocron
@date 		2018.10.10

This file prints the resulting numbers to the command line

Post about this code:
https://www.reddit.com/r/LongDistance/comments/9mgcol/oc_chat_statistics_from_telegram_using_python/

Inspiration:
https://www.reddit.com/r/LongDistance/comments/9jud8j/analysis_of_texts_from_a_long_distance/
"""

from __future__ import print_function

def _print_results(metrics):
    print("[ name: " + metrics["A"]["name"] + "]")
    print("total message count:     \t" + str(metrics["A"]["total_messages"]))
    print("total word count:        \t" + str(metrics["A"]["total_words"]))
    print("total character count:   \t" + str(metrics["A"]["total_chars"]))
    print("average word count:      \t" + str(metrics["A"]["avg_words"]))
    print("total unique words:      \t" + str(metrics["A"]["unique_words"]))
    print("average character count: \t" + str(metrics["A"]["avg_chars"]))

    if "urls" in metrics["A"]:
        print("used markdown in:        \t" + str(metrics["A"]["urls"]) + " messages")
        print("total urls in messages:  \t" + str(metrics["A"]["urls"]))
    if "photo" in metrics["A"]:
        print("total photos:            \t" + str(metrics["A"]["photo"]))
    for key in metrics["A"]["media"]:
        print("total " + str(key) + " count: \t\t" + str(metrics["A"]["media"][key]))

    print("")
    print("[ name: " + metrics["B"]["name"] + "]")
    print("total message count:     \t" + str(metrics["B"]["total_messages"]))
    print("total word count:        \t" + str(metrics["B"]["total_words"]))
    print("total character count:   \t" + str(metrics["B"]["total_chars"]))
    print("average word count:      \t" + str(metrics["B"]["avg_words"]))
    print("total unique words:      \t" + str(metrics["B"]["unique_words"]))
    print("average character count: \t" + str(metrics["B"]["avg_chars"]))
    if "urls" in metrics["B"]:
        print("used markdown in:        \t" + str(metrics["B"]["urls"]) + " messages")
        print("total urls in messages:  \t" + str(metrics["B"]["urls"]))
    if "photo" in metrics["B"]:
        print("total photos:            \t" + str(metrics["B"]["photo"]))
    for key in metrics["B"]["media"]:
        print("total " + str(key) + " count: \t\t" + str(metrics["B"]["media"][key]))

    print("")
    print("[ combined stats ]")
    print("total message count:     \t" + str(metrics["total"]))