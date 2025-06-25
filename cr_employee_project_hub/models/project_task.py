# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api
import random

class HrEmployee(models.Model):
    _inherit = ["project.task"]

    recommended_for = fields.Many2many(string="Training Records", comodel_name="hr.employee")
    skill_match_percent = fields.Float(string='Skill Percent')
    assigned_to_ids = fields.Many2many(string='Assigned To', comodel_name="res.partner")
    task_completed_employee = fields.Char(string='Task Completed Employee', related='recommended_for.name', domain=[('recommended_for.training_record_ids.status', '=', 'completed')])

    def suggest_task_assignees(self):
        employee_recs = self.env['employee.training.record'].search([('status', '=', 'completed')])
        if len(list(employee_recs)) <= 5:
            return{
                'name': 'Task Assignees',
                'type': 'ir.actions.act_window',
                'res_model': 'employee.training.record',
                'view_mode': 'tree',
                'domain': [('id', 'in', employee_recs.ids)]
            }
        else :
            random_employees = random.sample(employee_recs.ids, 2)
            return{
                'name': 'Task Assignees',
                'type': 'ir.actions.act_window',
                'res_model': 'employee.training.record',
                'view_mode': 'tree',
                'domain': [('id', 'in', random_employees)]
            }

    @api.onchange('project_id')
    def reset_assignees_on_project_update(self):
        self.user_ids = None