# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api


class TrainingSession(models.Model):
    _name = 'employee.training.record'
    _description = 'employee training record model'

    employee_id = fields.Many2one(string="Employee", comodel_name="hr.employee")
    training_id = fields.Many2one(string="Training", comodel_name="training.session")
    status = fields.Selection([('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], string="Status")
    feedback = fields.Text(string="Feedback")
    employee_job_title = fields.Char(string='Job Title', related='employee_id.job_title')
