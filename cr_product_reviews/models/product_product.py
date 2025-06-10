# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = ['product.product']

    review_ids = fields.One2many(comodel_name='product.review', inverse_name='product_id', string='Reviews')
