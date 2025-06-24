# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = ["hr.employee"]

    training_record_ids = fields.One2many(string="Training Records", comodel_name="employee.training.record", inverse_name="employee_id")
    certified_skills = fields.Char(string='Certified Skills', compute="count_completed_trainings")

    @api.depends('training_record_ids.status')
    def count_completed_trainings(self):
        print(self)
        for rec in self:
            print(self.status)
            print(self.feedback)