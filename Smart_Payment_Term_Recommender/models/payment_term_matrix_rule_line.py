# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
from odoo import models, fields, api

class PaymentTermMatrixRuleLine(models.Model):
    _name = "payment.term.matrix.rule.line"

    rule_id = fields.Many2one(comodel_name='payment.term.matrix.rule', string='Rules')
    operator = fields.Selection([('lt', '<'), ('le', '<='), ('eq', '='), ('gt', '>'), ('ge', '>='), ('between', 'Between')], string='Operator')
    value_1 = fields.Float(string='Value 1')
    value_2 = fields.Float(string='Value 2')
    score = fields.Float(string='Score')
    active = fields.Boolean(string='Active', default='True')