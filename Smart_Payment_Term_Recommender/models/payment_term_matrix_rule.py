# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
from odoo import models, fields, api

class PaymentTermMatrixRule(models.Model):
    _name = "payment.term.matrix.rule"

    matrix_id = fields.Many2one(comodel_name='payment.term.matrix', string='Matrix')
    rule_line_ids = fields.One2many(comodel_name='payment.term.matrix.rule.line', inverse='rule_id', string='Rule Line')

