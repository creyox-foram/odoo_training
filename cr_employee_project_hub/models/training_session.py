# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class TrainingSession(models.Model):
    _name = 'training.session'
    _description = 'training session model'

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    trainer = fields.Char(string="Trainer")
    description = fields.Text(string="Description")
    record_ids = fields.One2many(string="Employees", comodel_name="employee.training.record", inverse_name="training_id")

    def show_all_participants(self):
        emps = []
        for rec in self.record_ids:
            emps.append(rec.employee_id.id)
        return {
            'name': 'Employees',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee',
            'view_mode': 'tree',
            'target': 'new',
            'domain': [('id', 'in', emps)]
        }