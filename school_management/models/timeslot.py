from odoo import api, fields, models


class SchoolTimeslots(models.Model):
    _name = "school.timeslot"
    _description = "School Timeslots"

    name = fields.Char(string='Time Slot', required=True)
