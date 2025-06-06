# -*- coding: utf-8 -*-
# Part of Creyox Technologies.

from odoo import models, fields

class Author(models.Model):
    _name = "author_model"
    _description = "Author data"

    name = fields.Char(String = "Name : ")
    description = fields.Text(string= "Description : ")
    age = fields.Integer(String = "Age : ")
    salary = fields.Float(String = "Salary : ")
    feedback = fields.Html(String = "Feedback : ")
    birthdate = fields.Date(String = "Birth Date : ")
    isIndian = fields.Boolean(String = "Is Indian : ")
    image = fields.Image(String = "Choose Image : ")