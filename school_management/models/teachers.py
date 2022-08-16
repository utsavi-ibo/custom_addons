# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "Teachers"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], required=True, default='other')
    time_table = fields.One2many('teacher.timetable', 'name')


