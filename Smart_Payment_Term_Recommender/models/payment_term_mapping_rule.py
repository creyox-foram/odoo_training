# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
from odoo import models, fields, api

class PaymentTermMappingRule(models.Model):
    _name = "payment.term.mapping.rule"

    score_min = fields.Integer(string="Min Score")
    score_max = fields.Integer(string="Max Score")
    payment_term_id = fields.Many2one(comodel_name='account.payment.term', string='Payment Term')
    active = fields.Boolean(string='Active')

