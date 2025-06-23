# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = ["project.task"]

    recommended_for = fields.Many2many(string="Training Records", comodel_name="hr.employee")
    skill_match_percent = fields.Float(string='Skill Percent')
    assigned_to_ids = fields.Many2many(string='Assigned To', comodel_name="res.partner")