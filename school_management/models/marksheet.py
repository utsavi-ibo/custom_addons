# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

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
    each_total = fields.Integer()
    semester = fields.Selection([
        ('sem1', 'Semester 1'),
        ('sem2', 'Semester 2'),
    ], required=True, default='sem1')
    grand_total = fields.Float(string="Total Marks", compute="total_marks", store=True)
    final_percentage = fields.Float(string="Percentage", compute="percentage")
    state = fields.Selection([('draft', 'Draft'), ('pass', 'Pass'), ('fail', 'Fail')],
                             default="draft", string='Status')
    remark = fields.Char(string="Remark")
    # result = fields.Char(string="Result")

    def reset_marks(self):
        if self.state == "pass":
            self.state = "draft"
            # self.physics = 0.0
            # self.chemistry = 0.0
            # self.maths = 0.0
            # self.biology = 0.0
            # self.english = 0.0
            # self.write({'result': 'Reset to draft'})
            # class_env = self.env["student.class"]
            # class_id = class_env.browse(self.student_class)
            # print(class_id)
            # class_name = class_env.search([self.student_class, '=', "student_class"])
            # print(class_name)
            class_id = self.env["student.class"].browse(self.student_class.id)
            class_id.write({'room_no': 10})

        else:
            raise UserError("State should be in pass")

    def final_result(self):
        fail_students = self.search([("grand_total", "<", 400)])
        print(fail_students)
        pass_students = self.search([("grand_total", ">=", 400)])
        print(pass_students)
        if fail_students:
            for each in fail_students:
                each.state = "fail"
                # each.result = "Unsuccessful"
        if pass_students:
            for each in pass_students:
                each.state = "pass"
                # each.result = "successful"

    def create_record(self):
        new_student_obj = self.env['student.details']

        def id_generator():
            search_id = new_student_obj.search([], order="id desc", limit=1)
            new_name = search_id.name.split(" ")
            number = new_name[-1]
            number = int(number) + 1
            final_name = new_name[0] + " " + str(number)
            return final_name

        def email_generator():
            final_name = id_generator()
            email_id = final_name.split(" ")
            new_email = "{}_{}@gmail.com".format(email_id[0], email_id[1])
            return new_email

        values = {
            'name': id_generator(),
            'gender': 'female',
            'email' : email_generator()

        }
        new_student_create = new_student_obj.create(values)
        print(new_student_create)

    def orm_method(self):
        # print("self id.....", self.search([]))
        student_name = self.env["student.details"].search([])
        print("before update.....", student_name.mapped("admission_date"))
        student_name.mapped(lambda student: student.update({"admission_date": student.admission_date + timedelta(days=4)}))
        print("updated...", student_name.mapped("admission_date"))
        # print("unfiltered, unsorted...", student_name)
        # print("sorted...", student_name.sorted(lambda roll_call: roll_call.roll_no).mapped("name"))
        # print("filtered...", student_name.filtered(lambda gender: gender.gender == "male").mapped("name"))

    @api.depends("physics", "chemistry", "maths", "biology", "english")
    def total_marks(self):
        for each_mark_sheet in self:
            each_mark_sheet.grand_total = each_mark_sheet.physics + \
                                          each_mark_sheet.chemistry + \
                                          each_mark_sheet.maths + \
                                          each_mark_sheet.biology + \
                                          each_mark_sheet.english

    @api.depends("total", "grand_total")
    def percentage(self):
        # self.each_total = self.total/5
        for each_percent in self:
            each_percent.each_total = each_percent.total/5
            if each_percent.total and each_percent.grand_total:
                each_percent.final_percentage = (each_percent.grand_total / each_percent.total) * 100
            else:
                each_percent.final_percentage = 0.0

    @api.constrains("physics", "chemistry", "maths", "biology", "english")
    def _check_negative_marks(self):
        if (self.physics < 0 or self.chemistry < 0 or self.maths < 0 or self.biology < 0
                or self.english < 0):
            raise ValidationError('Marks cannot be negative')
