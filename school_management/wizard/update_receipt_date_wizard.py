# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime

class UpdateDateWizard(models.TransientModel):
    _name = "update.receipt.date.wizard"
    _description = "Update Date"

    update_receipt_date = fields.Datetime(string="Update Date", default=fields.Datetime.now(), required= True)

    def updated_receipt_date(self):
        # self.env.context.get("active_ids")._compute_date_deadline()
        select_ids = self.env.context.get("active_ids")
        purchase_env = self.env["purchase.order"]
        for each in select_ids:
            purchase_env.browse(each).update({'date_planned': self.update_receipt_date})
        print(self.env.context.get("active_ids"))
        # print(self.env.context)
        print(self.update_receipt_date)
        return True
