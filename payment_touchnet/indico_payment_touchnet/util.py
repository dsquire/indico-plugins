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
    if not isinstance(form.data, int) and form.data > 0:
        raise ValidationError(_('Invalid Site Id'))


def validate_key(form, field):
    # TODO: Don't hardcode the min length
    if len(form.data) < 10:
        raise ValidationError(_('Key must be longer than 10 bytes'))
