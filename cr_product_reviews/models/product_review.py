# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class ProductReview(models.Model):
    _name = "product.review"
    _description = "Product Review Model"

    product_id = fields.Many2one('product.product', string='Product')
    customer_id = fields.Many2one('res.partner', string='Customer')
    rating = fields.Integer(string='Rating', widget='rating')
    comment = fields.Text(string='Comment')
    review_date = fields.Date(string='Review Date')
    is_approved = fields.Boolean(string='Is Approved')

    @api.constrains('rating')
    def check_rating_under_5(self):
        if not (self.rating  >= 0 and self.rating <= 5):
            raise ValueError('Rating should be 1-5 !!')