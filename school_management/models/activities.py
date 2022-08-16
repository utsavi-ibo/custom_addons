from odoo import api, fields, models


class SchoolActivities(models.Model):
    _name = "student.activities"
    _description = "School Activities"

    name = fields.Char(string='Extracurricular Activities', required=True)
    percent = fields.Integer(string='Percentage Associated')
