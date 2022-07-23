# -*- coding: utf-8 -*-
# Developed by nu-civilisation. See LICENSE file for full copyright and licensing details.

import uuid
from odoo import api
from odoo import fields
from odoo import models


class SaleVouchers(models.Model):
    _name = 'sale.vouchers'
    _description = 'Sale Vouchers'
    _rec_name = 'voucher_code'
    # ...Uses the field voucher_code as the record's name in the breadcrumbs.

    voucher_code = fields.Char(string='Voucher-Code', required=True, index=True, readonly=True, default=lambda self: str(uuid.uuid4()))
    # ...Deliberately use UUID v4 to guarantee randomness.
    user_id = fields.Many2one(comodel_name='res.users', string='User', index=True)
    reason = fields.Char(string='Reason', index=True)
    tackled = fields.Datetime(string='Tackled', required=True, readonly=True, copy=False, default=lambda self: fields.Datetime.now())
    status = fields.Selection(selection=[
        (' ', 'unused'),
        ('o', 'validated'),
        ('x', 'invalidated'),
    ], index=True, default=' ')

    @api.model
    def get(self, voucherCode):
        records = self.sudo().search(args=[('voucher_code', '=', voucherCode)])
        for record in records:
            return record
        return None

    def isUnused(self):
        for record in self:
            return record == ' '

    def isValidated(self):
        for record in self:
            return (record == 'o')

    def isInvalidated(self):
        for record in self:
            return (record == 'x')

    def validate(self):
        for record in self:
            record.status = 'o'
            record.tackled = fields.Datetime.now()

    def invalidate(self):
        for record in self:
            record.status = 'x'
            record.tackled = fields.Datetime.now()
