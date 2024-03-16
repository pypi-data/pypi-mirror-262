# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from symposium.connectors.openai import get_openai_client, openai_complete, openai_message
from grammateus.entities import Grammateus

grammateus = Grammateus(origin='anthropic', location='convers.log')
oai = get_openai_client()
messages = [
    {'role': 'user','content': 'Hello'}
]
openai_message(
    client=oai,
    messages=messages,
    recorder=grammateus
)
response=openai_message.content[0].text

prompt = 'Hello'
completion = openai_complete(
    oai,
    prompt,
    recorder=grammateus
)


if __name__ == "__main__":
    print("ok")

