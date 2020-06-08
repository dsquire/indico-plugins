# This file is part of the Indico plugins.
# Copyright (C) 2002 - 2019 CERN
#
# The Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License;
# see the LICENSE file for more details.

from __future__ import unicode_literals

from flask_pluginengine import render_plugin_template

from wtforms.fields.core import StringField, IntegerField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Optional

from indico.core.plugins import IndicoPlugin, url_for_plugin
from indico.modules.events.payment import (PaymentEventSettingsFormBase, PaymentPluginMixin,
                                           PaymentPluginSettingsFormBase)
from indico.util.string import remove_accents, unicode_to_ascii
from indico.web.forms.validators import UsedIf

from indico_payment_touchnet import _
from indico_payment_touchnet.blueprint import blueprint
from indico_payment_touchnet.util import validate_site_id, validate_key


class PluginSettingsForm(PaymentPluginSettingsFormBase):
    url = URLField(_('Touchnet uPay API URL'), [DataRequired()], description=_('URL of the uPay HTTP API.'))


class EventSettingsForm(PaymentEventSettingsFormBase):
    site_id = IntegerField(_('Site Id'), [UsedIf(lambda form, _: form.enabled.data), DataRequired(),
                                          validate_site_id],
                           description=_('TouchNet uPay Site Id associated with event.'))

    validation_key = StringField(_('Validation Key'), [UsedIf(lambda form, _: form.enabled.data), DataRequired(),
                                                       validate_key],
                                 description=_('TouchNet validation key associated with event.'))

    posting_value = StringField(_('Posting Value'), [UsedIf(lambda form, _: form.enabled.data), DataRequired(),
                                                     validate_key],
                                description=_('TouchNet posting value associated with event.'))


class TouchnetPaymentPlugin(PaymentPluginMixin, IndicoPlugin):
    """Touchnet

    Provides a payment method using the Touchnet uPay API.
    """
    configurable = True
    settings_form = PluginSettingsForm
    event_settings_form = EventSettingsForm
    # TODO: need to add plugin level setting to capture the c20210
    default_settings = {'method_name': 'Touchnet',
                        'url': 'https://test.secure.touchnet.net:8443/c20210test_upay/web/index.jsp'}
    default_event_settings = {'enabled': False,
                              'method_name': None,
                              'validation_key': None,
                              'posting_value': None}

    def init(self):
        super(TouchnetPaymentPlugin, self).init()
        # self.template_hook('event-manage-payment-plugin-before-form', self._get_encoding_warning)

    @property
    def logo_url(self):
        return url_for_plugin(self.name + '.static', filename='images/logo.png')

    def get_blueprints(self):
        return blueprint

    def adjust_payment_form_data(self, data):
        event = data['event']
        registration = data['registration']
        data['item_name'] = '{}: registration for {}'.format(
            unicode_to_ascii(remove_accents(registration.full_name, reencode=False)),
            unicode_to_ascii(remove_accents(event.title, reencode=False))
        )
        data['return_url'] = url_for_plugin('payment_touchnet.success', registration.locator.uuid, _external=True)
        data['cancel_url'] = url_for_plugin('payment_touchnet.cancel', registration.locator.uuid, _external=True)
        data['notify_url'] = url_for_plugin('payment_touchnet.notify', registration.locator.uuid, _external=True)

    # def _get_encoding_warning(self, plugin=None, event=None):
    #     if plugin == self:
    #         return render_plugin_template('event_settings_encoding_warning.html')
