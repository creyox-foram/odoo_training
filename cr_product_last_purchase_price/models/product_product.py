# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class PurchasePrice(models.Model):
    _inherit = ['product.product']

    last_purchase_price = fields.Float(string='Last Purchase Price')
