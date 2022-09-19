from odoo import api, fields, models


class SchoolBranch(models.Model):
    _name = "school.branch"
    _description = "School Branch"
    _rec_name = "school_branch"

    name = fields.Char(string='Branch Name', required=True)
    school_branch = fields.Char(string='Branch', readonly=True)

    @api.model
    def create(self, vals):
        sequence_id = self.env.ref("school_management.seq_branch").ids
        # purchase_id = self.env['purchase.order']
        # search_id = purchase_id.search([])
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

        vals.update({'school_branch': vals.get("name") + "/" + record_id})
        return super(SchoolBranch, self).create(vals)
