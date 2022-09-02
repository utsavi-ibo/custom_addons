# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import timedelta
from .purchase import PurchaseOrder as p


class StudentDetails(models.Model):
    _name = "student.details"
    _description = "Student Details"
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, translate=True)
    email = fields.Char(string='Email')
    reference = fields.Char(string='Reference ID', readonly=True)
    reference_1 = fields.Char(string='Purchase Reference ID')
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'other'),
    ], default='other')
    birth_date = fields.Datetime(string="D.O.B")
    roll_no = fields.Integer(string='Roll No', tracking=True, copy=False)
    admission_date = fields.Date(string="Date of Admission")
    mark_sheet_ids = fields.One2many('student.marks', 'name')
    activities_ids = fields.Many2many('student.activities', string="Extracurricular Activities")
    student_class_id = fields.Many2one('student.class', string="Class")
    teacher = fields.Many2one(string="Class Teacher", related="student_class_id.teacher")
    _sql_constraints = [('roll_no_unique', 'unique(roll_no)', 'This roll No already exist')]
    dob_difference = fields.Integer(string='Difference', default=4)
    purchase_count = fields.Integer(string="PO", compute="compute_purchase_count")

    def compute_purchase_count(self):
        for each in self:
            each.purchase_count = self.env["purchase.order"].search_count([("student_purchase.name", "=", each.name)])

    @api.model
    def default_get(self, vals):
        res = super(StudentDetails, self).default_get(vals)
        res['gender'] = "female"
        res['admission_date'] = fields.Date.today()
        # print("fields----", vals)
        # print("res----", res)
        return res

    @api.model
    def birthday_reminder(self):
        today_birthday = self.search([("birth_date", "=", fields.Date.today())])
        if today_birthday:
            print("hiiiiii")
            for each in today_birthday:
                each.message_post(body="Happy Birthday {}".format(each.name), subject="Birthday Wish")

    def copy(self, default={}):
        default["birth_date"] = self.birth_date + timedelta(days=self.dob_difference)
        return super(StudentDetails, self).copy(default)

    @api.model
    def create(self, vals):
        sequence_id = self.env.ref("school_management.seq_students").ids
        purchase_id = self.env['purchase.order']
        search_id = purchase_id.search([])
        # print(search_id)
        # for each in search_id:
        #     print(each.student_purchase)
        #     if each.student_purchase and each.student_purchase == vals.get("name"):
        #         # search_year = each.purchase_year
        #         print(each.purchase_year)
        if sequence_id:
            record_id = self.env["ir.sequence"].browse(sequence_id).next_by_id()
        else:
            record_id = '/'

        vals.update({'reference': vals.get("name") + "/" + record_id})
        return super(StudentDetails, self).create(vals)

    def test_year(self):
        purchase_id = self.env['purchase.order']
        search_id = purchase_id.search([])
        print(search_id)
        for each in search_id:
            if each.purchase_year:
                print(each.purchase_year)

    def button_purchase_order(self):
        if self.purchase_count == 1:
            return {
                'name': "Purchase Order",
                'view_mode': 'form',
                'res_model': 'purchase.order',
                # 'view_id': self.env.ref('purchase.purchase_order_form').id,
                'type': 'ir.actions.act_window',
                'domain': [("student_purchase.name", "=", self.name)],
                'target': 'main',
                'res_id': int(self.env['purchase.order'].search([("student_purchase", "=", self.name)]))
            }
        elif self.purchase_count == 0:
            return {
                'name': "Purchase Order",
                'view_mode': 'form',
                'res_model': 'purchase.order',
                # 'view_id': self.env.ref('purchase.purchase_order_form').id,
                # 'type': 'ir.actions.act_window',
                # 'domain': [("student_purchase.name", "=", self.name)],
                'target': 'main',
                # 'res_id': int(self.env['purchase.order'].search([("student_purchase", "=", self.name)]))
                'context': {'create': False}
            }
        else:
            return {
                'name': "Purchase Order",
                'view_mode': 'tree,form',
                'res_model': 'purchase.order',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'domain': [("student_purchase.name", "=", self.name)]
            }
