# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class Product(models.Model):
    _name = 'product_model'
    _description = 'Product Model'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    price = fields.Float(string='Price')
    total_quantity = fields.Float(string='Total Quantity')
    total_stock = fields.Integer(string='Total Stock')
    category_id = fields.Many2one('category_model', string='Category')
    image = fields.Binary(string='Image')
    supplier_id = fields.Many2one('supplier_model', string="Supplier")
    active = fields.Boolean(string='Active', default='True')

    @api.onchange('total_quantity')
    def setTotalStock(self):
        self.total_stock = self.total_quantity