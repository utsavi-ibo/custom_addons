# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student Details"
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, translate=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], default='other')
    birth_date = fields.Date(string="D.O.B")
    roll_no = fields.Integer(string='Roll No', tracking=True)
    admission_date = fields.Date(string="Date of Admission")
    mark_sheet_ids = fields.One2many('student.marks', 'name')
    activities_ids = fields.Many2many('student.activities', string="Extracurricular Activities")
    student_class_id = fields.Many2one('student.class', string="Class")
    teacher = fields.Many2one(string="Class Teacher", related="student_class_id.teacher")
    _sql_constraints = [('roll_no_unique', 'unique(roll_no)', 'This roll No already exist')]

    @api.model
    def default_get(self, vals):
        res = super(StudentDetails, self).default_get(vals)
        res['gender'] = "female"
        res['admission_date'] = fields.Date.today()
        print("fields----", vals)
        print("res----", res)
        return res

    @api.model
    def birthday_reminder(self):
        today_birthday = self.search([("birth_date", "=", fields.Date.today())])
        if today_birthday:
            print("hiiiiii")
            for each in today_birthday:
                each.message_post(body="Happy Birthday {}".format(each.name), subject="Birthday Wish")