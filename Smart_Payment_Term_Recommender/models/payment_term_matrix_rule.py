# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
from odoo import models, fields, api

class PaymentTermMatrixRule(models.Model):
    _name = "payment.term.matrix.rule"

    matrix_id = fields.Many2one(comodel_name='payment.term.matrix', string='Matrix')
    operator = fields.Selection([('lt', '<'), ('le', '<='), ('eq', '='), ('gt', '>'), ('ge', '>='), ('between', 'Between')], string='Operator')
    value_1 = fields.Float(string='1st Value')
    value_2 = fields.Float(string='2nd Value')
    type = fields.Selection([('numeric', 'Numeric'), ('percent', 'Percent'), ('monetary', 'Monetary'), ('ratio', 'Ratio'), ('days', 'Days'), ('count', 'Count')], string='Type')
    score = fields.Float(string='Score')

