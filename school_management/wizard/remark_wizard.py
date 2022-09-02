# -*- coding: utf-8 -*-
from odoo import api, fields, models


class RemarkWizard(models.TransientModel):
    _name = "remark.display.wizard"
    _description = "Display Remark"

    remark = fields.Char(string='Remarks', required=True)

    def display_remark(self):
        student_marksheet = self.env["student.marks"]
        # print(student_marksheet.browse())
        # print(".........context", self.env.context)
        current_id = self.env.context.get('active_id')
        student_marksheet.browse(current_id).remark = self.remark
        # print(student_marksheet.browse(current_id).remark)
        # if not student_marksheet.remark:
        #     student_marksheet.remark = self.remark
        # print(student_marksheet.remark)
        # print("Executing")
        return True
