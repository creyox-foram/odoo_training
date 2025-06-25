# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = ["hr.employee"]

    training_record_ids = fields.One2many(comodel_name="employee.training.record", inverse_name="employee_id", string="Training Records")
    certified_skills = fields.Char(string='Certified Skills', compute="count_completed_trainings")
    status = fields.Selection([('active', 'Active'), ('inactive', 'In Active'), ('onleave', 'On Leave')],string="String")

    @api.depends('training_record_ids.status')
    def count_completed_trainings(self):
        print(self)
        print("employee training record compute")
        self.certified_skills = "completed trainings"

    def show_training_history(self):
        return {
            'name': 'Training History',
            'type': 'ir.actions.act_window',
            'res_model': 'employee.training.record',
            'view_mode': 'tree',
            'target': 'new',
            'domain': [('employee_id', '=', self.id)]
        }

    def toggle_status(self):
        if self.status == False:
            self.status = 'active'
        elif self.status == 'active':
            self.status = 'inactive'
            employee_id = self.id
            if self.status == 'inactive':
                self.env['employee.training.record'].browse(employee_id).write({'status': 'pause'})
                print("done")
        elif self.status == 'inactive':
            self.status = 'active'


