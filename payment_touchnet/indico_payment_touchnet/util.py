# This file is part of the Indico plugins.
# Copyright (C) 2002 - 2019 CERN
#
# The Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License;
# see the LICENSE file for more details.

from __future__ import unicode_literals

from wtforms import ValidationError

from indico_payment_touchnet import _


def validate_site_id(form, field):
    # TODO: Consider providing better validation here
    pass


def validate_key(form, field):
    # TODO: Don't hardcode the min length
    pass
