from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    eb_employee_id = fields.Many2one('employee.ebm', string="Employee")
    eb_user_id = fields.Many2one('user.ebm', string="User")
