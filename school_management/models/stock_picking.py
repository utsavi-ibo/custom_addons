# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, timedelta

class Picking(models.Model):
    _inherit = ["stock.picking"]

    # purchase_year = fields.Char(string='Year of Purchase', required=True)
    # student_purchase = fields.Many2one('student.details', string='Student')
    school_branch_id = fields.Many2one('school.branch', string='Branch')

    def _compute_date_deadline(self):
        values = super(Picking, self)._compute_date_deadline()
        self.scheduled_date = self.env["purchase.order"].search([("name", "=", self.origin)]).date_planned
        self.date_deadline = self.scheduled_date + timedelta(days=2)
        # print(self.env["purchase.order"].search([("name", "=", self.origin)]).date_planned)
        # self.scheduled_date = self.env["purchase.order"].search([("name", "=", self.origin)]).date_planned
        return values

    # def button_confirm(self):
    #     search_ids = self.env['student.details'].search([])
    #     self.update({"name": self.student_purchase.reference + "/" + self.purchase_year + "/" + self.name})
    #     for each in search_ids:
    #         if each.name == self.student_purchase.name:
    #             each.reference_1 = self.name
    #             break
    #
    #     #         # print(self.name)
    #     res = super(PurchaseOrder, self).button_confirm()
    #     return res
    #
    # def _prepare_picking(self):
    #     res = super(PurchaseOrder, self)._prepare_picking()
    #     res.update({'branch': self.school_branch.school_branch})
    #     return res


