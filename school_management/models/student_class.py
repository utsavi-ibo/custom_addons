# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentClass(models.Model):
    _name = "student.class"
    _description = "Student Class"
    _rec_name = "student_class"

    student_class = fields.Char(string="Class", required=True)
    room_no = fields.Integer(string="Room No", required=True)
    floor = fields.Integer(string="Floor", required=True)
    teacher = fields.Many2one("school.teacher", string="Class Teacher", required=True)
    time_table = fields.One2many('teacher.timetable', 'student_class')
    student_name = fields.One2many('student.details', 'student_class_id')


