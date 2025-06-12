# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _description = 'inherited the product.template model'

    reviews = fields.Char(string='Review ids', compute='get_reviews')
    average_rating = fields.Float(string='Average Rating', compute='calc_average_rating')
    review_ids = fields.Html(string='Reviews')

    @api.depends('reviews')
    def calc_average_rating(self):
        print(self)
        print("i am average")
        self.average_rating = 0

    def get_reviews(self):
        print(self)
        # self.product_id, '=', self.tem
        product_record = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        print("product record : ", product_record)

        review_ids = self.env['product.review'].search([('product_id', '=', product_record.id)])
        print(review_ids)

        self.reviews = review_ids
        # self.review_ids = f"""
        #     <div>
        #     <p>Reviewer: {review_ids.customer_id.name}</p>
        #     <p>Rating: {review_ids.rating}</p>
        #     <p>Comment: {review_ids.comment}</p>
        #     </div>
        # """

    @api.onchange('reviews')
    def format_reviews(self):
        print(self)
        print("i am inside ")

        product_record = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        print("product record : ", product_record)

        review_ids = self.env['product.template'].search(['reviews', '=', product_record.id])

        for review in review_ids:
            if review:
                value =  {
                    'reviews': f"""
                        <p>Reviewer: {review.customer_id.name}</p>
                        <p>Rating: {review.rating}</p>
                        <p>Comment: {review.comment}</p>
                    """
                }
                self.env['product.template'].create(value)