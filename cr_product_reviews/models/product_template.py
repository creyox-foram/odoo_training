# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _description = 'inherited the product.template model'

    review_ids = fields.Char(string='Reviews', compute='get_review_ids')
    average_rating = fields.Float(string='Average Rating', compute='calc_average_rating')

    def calc_average_rating(self):
        print(self)
        self.average_rating = 0

    @api.depends('name')
    def get_review_ids(self):
        print(self.env['product.product'].search([]))
        print("i am in function")
        self.review_ids = 0