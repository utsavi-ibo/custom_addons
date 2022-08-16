# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolTeacher(models.Model):
    _name = "teacher.timetable"
    _description = "Teacher Timetable"

    name = fields.Many2one('school.teacher', string='Name', required=True)
    time_slot = fields.Many2one('school.timeslot', string="Time Slot", required=True)
    week_day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    ], string='Day', required=True, default='Monday')
    subject_name = fields.Selection([
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('maths', 'Maths'),
        ('english', 'English'),
    ], required=True, default='Physics')
    student_class = fields.Many2one('student.class', string='Class', required=True)




