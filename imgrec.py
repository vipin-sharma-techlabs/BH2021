"""
A simple Image recognization engine.
"""
import argparse
import json
import os

import boto3
from botocore.config import Config

my_config = Config(
    region_name = 'us-west-2',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

# Image

class ImageRecognizer(object):

    def __init__(self, imgpath):
        assert os.path.exists(imgpath)
        self.img = imgpath
        self._response = None

    @property
    def response(self):
        if self._response:
            return self._response
        self._response = self.recognize()
        return self._response

    def recognize(self):
        # Read image content
        with open(self.img, 'rb') as document:
            imageBytes = bytearray(document.read())

        # Amazon Rekognition client
        rekognition = boto3.client('rekognition', config=my_config)

        # Call Amazon Rekognition
        response = rekognition.detect_protective_equipment(
                Image={'Bytes': imageBytes},
                SummarizationAttributes={
                    'MinConfidence': 90,
                    'RequiredEquipmentTypes': [
			'HAND_COVER', 'FACE_COVER', 'HEAD_COVER'
			]
                    }
                )
        return response

    def summary(self):
        print(self.response["Summary"])

    def dump_summary(self):
        ofile = os.path.splitext(self.img)[0] + '.json'
        with open(ofile, "w+") as f:
            f.write(json.dumps(self.response))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--image', help="Path to image file", required=True)
    parser.add_argument(
        '-j', '--json', action='store_true',
        help="Export summary in json")

    args = parser.parse_args()

    ir = ImageRecognizer(args.image)
    if args.json:
        ir.dump_summary()

    ir.summary()



if __name__ == '__main__':
    main()
