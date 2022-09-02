# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_year = fields.Char(string='Year of Purchase', required=True)
    student_purchase = fields.Many2one('student.details', string='Student')

    def button_confirm(self):
        search_ids = self.env['student.details'].search([])
        self.update({"name": self.student_purchase.reference + "/" + self.purchase_year + "/" + self.name})
        for each in search_ids:
            if each.name == self.student_purchase.name:
                each.reference_1 = self.name

                # print(self.name)
        res = super(PurchaseOrder, self).button_confirm()
        return res

