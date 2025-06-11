# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _description = 'inherited the product.template model'

    review_ids = fields.Char(string='Reviews', compute='show_reviews')
    average_rating = fields.Float(string='Average Rating', compute='calc_average_rating')

    @api.depends('review_ids')
    def calc_average_rating(self):
        print(self)
        print("i am average")
        self.average_rating = 0

    def show_reviews(self):
        print(self)
        # self.product_id, '=', self.tem
        product_record = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        print("product record : ",product_record)

        review_ids = self.env['product.review'].search([('product_id', '=', product_record.id)])
        print(review_ids)

        self.review_ids = review_ids

        template = self.env.ref('cr_product_reviews.custom_template_id')
        rendered_template = template.render(review_ids)
        return rendered_template