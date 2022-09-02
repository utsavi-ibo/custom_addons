# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


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

    @api.model
    def create(self, vals):
        if vals.get('floor'):
            vals['room_no'] = vals.get('floor') + 4
        school_class = super(StudentClass, self).create(vals)
        return school_class

    def write(self, vals):
        vals['room_no'] = 8
        school_class = super(StudentClass, self).write(vals)
        return school_class

    def unlink(self):
        if self.teacher.name == "Seema":
            raise ValidationError('You can not delete this record.')
        # With the non plannified picking, draft moves could have some move lines.
        return super(StudentClass, self).unlink()






