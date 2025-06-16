# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _description = 'inherited the product.template model'

    reviews = fields.Char(string='Review ids', compute='get_review_ids', store='True')
    review_ids = fields.Html(string='Reviews', compute='format_reviews')


    def get_review_ids(self):
        product_record = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        review_ids = self.env['product.review'].search([('product_id', '=', product_record.id)])
        self.reviews = review_ids


    @api.depends('reviews')
    def format_reviews(self):
        product_record = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        review_ids = self.env['product.review'].search([('product_id', '=', product_record.id)])
        value = """"""
        for review in review_ids:
            if review:
                value += f"""
                    <div>
                        <p> Reviewer: {review.customer_id.name}</p>
                        <p widget='rating'> Rating: {self.customize_rating_to_star(review.rating)}</p>
                        <p> Comment: {review.comment}</p>
                    </div>
                    <hr>
                """
            else:
                value = False
        self.review_ids = value


    def customize_rating_to_star(self, rating):
        return f"{'★' * int(rating)}{'☆' * (5 - int(rating))} ({rating}/5)"

