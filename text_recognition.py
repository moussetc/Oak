#!/usr/bin/env python3

import re
from names import POKEMON
import db

from google.cloud import vision
from google.cloud.vision import types
from fuzzywuzzy import process

time_pattern = re.compile('[0-9]+:[0-9]+:[0-9]+')


def build_image_url(image_url):
    source = types.ImageSource(image_uri=image_url)
    image = types.Image(source=source)
    return image


def build_image_file(image_file):
    with open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    return image


def detect_text(image_url):
    image = build_image_url(image_url)
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(image=image)
    return response.text_annotations[0].description.split('\n')


def find_fields(elements):
    boss = None
    time = None
    gym = None
    for e in elements:
        if time_pattern.search(e) is not None:
            time = e
            break
        for language in POKEMON:
            for p in POKEMON[language].values():
                if e.lower() in p.lower():
                    boss = p
                    break
        if e in db.all_gyms:
            gym = e
    return {'boss': boss, 'time': time, 'gym': gym}


def find_pokestop(elements):
    """
    Try to find the name of a pokestop that sort of matches one of the input strings in elements.
    """
    for e in elements:
        # First, try to find exact match
        if e in db.all_pokestops:
            return e
        else:
            # Then, try to find a close match 
            match = process.extractOne(e, db.all_pokestops, score_cutoff=80)
            if match is not None:
                return match[0]
    return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process text recognition')
    parser.add_argument('--image', '-i', help='Input image')
    args = parser.parse_args()

    run_quickstart(args.image)


if __name__ == '__main__':
    main()

