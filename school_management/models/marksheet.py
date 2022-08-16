# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class StudentMarks(models.Model):
    _name = "student.marks"
    _description = "Student Marks"

    name = fields.Many2one("student.details", string='Student Name')
    roll_no = fields.Integer(string="Roll No", related="name.roll_no")
    student_class = fields.Many2one("student.class", required=True)
    physics = fields.Float(string='Physics', required=True)
    chemistry = fields.Float(string='Chemistry', required=True)
    maths = fields.Float(string='Maths', required=True)
    biology = fields.Float(string='Biology', required=True)
    english = fields.Float(string='English', required=True)
    total = fields.Integer(string='Out of Marks', required=True)
    semester = fields.Selection([
        ('sem1', 'Semester 1'),
        ('sem2', 'Semester 2'),
    ], required=True, default='sem1')
    grand_total = fields.Float(string="Total Marks", compute="total_marks")
    final_percentage = fields.Float(string="Percentage", compute="percentage")
    state = fields.Selection([('draft', 'Draft'), ('pass', 'Pass'), ('fail', 'Fail')],
                             default="draft", string='Status')
    result = fields.Char(string="Result")

    def reset_marks(self):
        self.state = "draft"
        self.physics = 0.0
        self.chemistry = 0.0
        self.maths = 0.0
        self.biology = 0.0
        self.english = 0.0

    def final_result(self):
        if self.final_percentage < 35:
            self.state = "fail"
            self.result = "Unsuccessful"
        else:
            self.state = "pass"
            self.result = "Successful"

    @api.onchange("physics", "chemistry", "maths", "biology", "english")
    def total_marks(self):
        for each_mark_sheet in self:
            print("self_value======",self)
            print(each_mark_sheet)
            each_mark_sheet.grand_total = each_mark_sheet.physics + each_mark_sheet.chemistry + each_mark_sheet.maths + each_mark_sheet.biology + each_mark_sheet.english

    @api.depends("total", "grand_total")
    def percentage(self):
        for each_percent in self:
            if each_percent.total and each_percent.grand_total:
                each_percent.final_percentage = (each_percent.grand_total / each_percent.total) * 100
            else:
                each_percent.final_percentage = 0.0

    @api.constrains("physics", "chemistry", "maths", "biology", "english")
    def _check_negative_marks(self):
        if (self.physics < 0 or self.chemistry < 0 or self.maths < 0 or self.biology < 0
                or self.english < 0):
            raise ValidationError('Marks cannot be negative')







