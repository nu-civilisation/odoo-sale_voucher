# -*- coding: utf-8 -*-
# Developed by nu-civilisation. See LICENSE file for full copyright and licensing details.

import uuid
from odoo import api
from odoo import fields
from odoo import models


class SaleVouchers(models.Model):
    _name = "sale.vouchers"
    _description = "Sale Vouchers"

    voucher_uuid = fields.Char(string="Voucher-UUID", required=True, index=True, readonly=True, default=lambda self: str(uuid.uuid4()))
    # ...Deliberately use UUID v4 to guarantee randomness.
    user_ids = fields.Many2one(comodel_name="res.users", string="User")
    status = fields.Selection(selection=[
        (' ', 'unused'),
        ('o', 'validated'),
        ('x', 'invalidated'),
    ], default=' ')

    def isUnused(self):
        for record in self:
            return record == ' '

    def isValidated(self):
        for record in self:
            return (record == 'o')

    def isInvalidated(self):
        for record in self:
            return (record == 'x')

    @api.model
    def validate(self):
        for record in self:
            record.status = 'o'

    @api.model
    def invalidate(self):
        for record in self:
            record.status = 'x'
