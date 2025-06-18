from odoo import models, fields

# wizard for generating report
class ProductWizard(models.TransientModel):
    _name = 'product.review.report.wizard'

    date1 = fields.Date(string='Start Date')
    date2 = fields.Date(string='Ending Date')
    min_rating = fields.Selection([('0',0),('1',1),('2',2),('3',3),('4',4),('5',5)], string='Rating')
    approval_status = fields.Boolean(string='Approved Records')

    def generate_review_report(self):
        current_rec_id = self._context['current_product_template_id']
        product_template_record = self.env['product.review.report.wizard'].browse(int(current_rec_id))
        print(product_template_record)
        product_review_report_pdf = self.env.ref('cr_product_reviews.product_review_pdf_report_action_id', raise_if_not_found=False)
        return product_review_report_pdf.report_action(product_template_record)
