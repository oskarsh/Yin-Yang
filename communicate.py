#!/usr/bin/python

# This file enables the extension to communicate with yin-yang.

import sys
import json
import struct
from src import config


def encode_message(message_content: str):
    """
    Encode a message for transmission, given its content.
    :param message_content: a message as str
    """
    encoded_content = json.dumps(message_content).encode("utf-8")
    encoded_length = struct.pack('=I', len(encoded_content))
    # use struct.pack("10s", bytes)
    # to pack a string of the length of 10 characters

    return {'length': encoded_length,
            'content': struct.pack(str(len(encoded_content))+"s",
                                   encoded_content)}


# Send an encoded message to stdout.
def send_message(encoded_message):
    """
    Send a message.
    :param message: message as json
    """
    sys.stdout.buffer.write(encoded_message['length'])
    sys.stdout.buffer.write(encoded_message['content'])
    sys.stdout.buffer.flush()


# Read a message from stdin and decode it.
def get_message():
    raw_length = sys.stdin.buffer.read(4)

    if not raw_length:
        sys.exit(0)
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")

    return json.loads(message)


while True:
    message = get_message()
    if message == 'GetTheme':
        theme = config.get("firefoxActiveTheme")
        send_message(encode_message(theme))
