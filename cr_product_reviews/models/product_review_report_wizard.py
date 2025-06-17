from odoo import models, fields

# wizard for generating report
class ProductWizard(models.TransientModel):
    _name = 'product.review.report_wizard'

    date1 = fields.Date(string='Start Date')
    date2 = fields.Date(string='Ending Date')
    min_rating = fields.Selection([('0',0),('1',1),('2',2),('3',3),('4',4),('5',5)], string='Rating')
    approval_status = fields.Boolean(string='Approved Records')

    def generate_review_report(self):
        print(self)
        print(self.id)
        print(self._context['record_id'])
        product_review_report_pdf = self.env.ref('cr_product_reviews.product_review_pdf_report_action_id', raise_if_not_found=False)
        return product_review_report_pdf.report_action(self)
