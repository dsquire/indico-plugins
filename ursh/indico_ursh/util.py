# This file is part of the Indico plugins.
# Copyright (C) 2002 - 2019 CERN
#
# The Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License;
# see the LICENSE file for more details.

from __future__ import unicode_literals

import posixpath

import requests
from werkzeug.exceptions import ServiceUnavailable


def _get_settings():
    from indico_ursh.plugin import UrshPlugin
    api_key = UrshPlugin.settings.get('api_key')
    api_host = UrshPlugin.settings.get('api_host')

    if not api_key or not api_host:
        raise ServiceUnavailable('Not configured')

    return api_key, api_host


def request_short_url(original_url):
    api_key, api_host = _get_settings()
    headers = {'Authorization': 'Bearer {api_key}'.format(api_key=api_key)}
    url = posixpath.join(api_host, 'urls/')

    response = requests.post(url, data={'url': original_url, 'allow_reuse': True}, headers=headers)
    if response.status_code not in (400,):
        response.raise_for_status()

    data = response.json()
    return data['short_url']


def register_shortcut(original_url, shortcut):
    api_key, api_host = _get_settings()
    headers = {'Authorization': 'Bearer {api_key}'.format(api_key=api_key)}
    url = posixpath.join(api_host, 'urls', shortcut)

    response = requests.put(url, data={'url': original_url, 'allow_reuse': True}, headers=headers)
    if not (400 <= response.status_code < 500):
        response.raise_for_status()

    return response.json()


def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text) - len(suffix)]
