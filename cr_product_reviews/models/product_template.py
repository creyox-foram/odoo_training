# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = ['product.template']
    _description = 'inherited the product.template model'

    reviews = fields.Char(string='Review ids', compute='show_reviews', store='True')
    average_rating = fields.Float(string='Average Rating', compute='calc_average_rating')
    review_ids = fields.Html(string='Reviews', compute='format_reviews')

    @api.depends('reviews')
    def calc_average_rating(self):
        print(self)
        print("i am average")
        self.average_rating = 0

    def show_reviews(self):
        print("i am inside reviews")
        print(self)
        product_record = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        print("product record : ", product_record)

        review_ids = self.env['product.review'].search([('product_id', '=', product_record.id)])
        print('reviews : ',review_ids)

        self.reviews = review_ids


    @api.depends('reviews')
    def format_reviews(self):
        print("i am inside review format")
        print(self.id)
        product_record = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
        print(product_record)
        review_ids = self.env['product.review'].search([('product_id', '=', product_record.id)])
        print(review_ids)
        value = """"""
        for review in review_ids:
            if review:
                print(review.customer_id.name)
                print(review.rating)
                print(review.comment)
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
