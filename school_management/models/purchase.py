# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime


class PurchaseOrder(models.Model):
    _inherit = ["purchase.order"]

    purchase_year = fields.Char(string='Year of Purchase', required=True)
    student_purchase = fields.Many2one('student.details', string='Student')
    school_branch_id = fields.Many2one('school.branch', string='Branch')

    @api.depends("date_approve")
    def write(self, vals):
        # print(vals.get("date_approve"))
        if self.date_approve and vals.get("date_planned") is not None:
            # print(vals.get("date_approve"))
            # print(self.date_approve)
            # approve_date = datetime.strptime(self.date_approve, '%Y-%m-%d %H:%M:%S')
            # # order_date = datetime.strptime(vals.get("date_order"), '%Y-%m-%d %H:%M:%S')
            receive_date = datetime.strptime(str(vals.get("date_planned")), '%Y-%m-%d %H:%M:%S')
            if self.date_approve > receive_date or receive_date <= datetime.today():
                raise UserError("Receipt date can not be less than order deadline or today")
            else:
                vals['date_planned'] = vals.get("date_planned")
        return super(PurchaseOrder, self).write(vals)

    def button_confirm(self):
        vendor_id_list = []
        if self.date_order > self.date_planned:
            raise UserError("Receipt date can not be less than order deadline")
        # print(self.partner_id.name)
        # print(self.order_line.name)
        # print(self.order_line.product_id.id)
        # print(self.env['product.supplierinfo'].search(["name"]))
        # supplier_info = self.env['product.supplierinfo']
        # print(self.env['product.supplierinfo'].search([]).product_tmpl_id)
        # supplier_info_id = self.env['product.supplierinfo'].search([]).product_tmpl_id
        # for each in supplier_info_id:
        #     print(each.name)
        order_line_ids = self.order_line
        print(order_line_ids)
        for each in order_line_ids:
            # print(self.partner_id.id)
            # print(each.product_id.product_tmpl_id.id)
            vendor_id = self.env['product.supplierinfo'].search([("name", "=", self.partner_id.id),
                                                             ("product_tmpl_id", "=", each.product_id.product_tmpl_id.id)])
            if not vendor_id:
                vendor_id_list.append(each.product_id.default_code)
        if vendor_id_list:
            print(vendor_id_list)
            raise UserError("{} products are not present in the pricelist".format(vendor_id_list))

        # print(self.date_order)
        # purchase_list_product_ids = self.env['product.supplierinfo'].search([(self.partner_id.name, "=", "name"),
        #                                                                      (self.order_line.name, "=", self.id)])
        zero_product_ids = self.env['purchase.order.line'].search([("product_qty", "<=", 0.0),
                                                                    ("order_id", "=", self.id)])
        if zero_product_ids:
            raise UserError("Order can not be of zero or negative quantity")
        search_ids = self.env['student.details'].search([])
        self.update({"name": self.student_purchase.reference + "/" + self.purchase_year + "/" + self.name})
        for each in search_ids:
            if each.name == self.student_purchase.name:
                each.reference_1 = self.name
                break

        # if self.date_planned > self.date_order:
        #     raise UserError("Hii")
        #         # print(self.name)
        res = super(PurchaseOrder, self).button_confirm()
        return res

    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        res.update({'school_branch_id': self.school_branch_id.id})
        print(self.school_branch_id.id)
        return res

    def _prepare_invoice(self):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice()
        invoice_vals['school_branch_id'] = self.school_branch_id.id
        return invoice_vals

    def update_receipt_date(self):
        print(self.ids)
        filtered_records = self.filtered(lambda r: r.partner_id != self[0].partner_id)
        if filtered_records:
            raise UserError("The records are from different vendors")
        else:
            return {
                'name': "Update Receipt Date",
                'view_mode': 'form',
                # 'view_type': 'form',
                'res_model': 'update.receipt.date.wizard',
                # 'view_id': self.env.ref('purchase.purchase_order_form').id,
                'type': 'ir.actions.act_window',
                'context': {
                    'active_model': 'purchase.order',
                    'active_ids': self.ids
                },
                # 'domain': [("student_purchase.name", "=", self.name)],
                'target': 'new',
                # 'res_id': int(self.env['purchase.order'].search([("student_purchase", "=", self.name)]))
            }


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    school_branch_id = fields.Many2one('school.branch', string='Branch', related='order_id.school_branch_id')

