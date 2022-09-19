# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = ["account.move"]

    school_branch_id = fields.Many2one('school.branch', string='Branch')


