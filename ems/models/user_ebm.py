from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class UserEBM(models.Model):
    _name = 'user.ebm'
    _description = 'User'
    _rec_name = 'name'

    user_id = fields.Char(string='User ID', readonly=True)
    name = fields.Char(string='Name' ,required=True)
    phone = fields.Char(string="Phone", size=10)
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    customer_id = fields.Many2one('customer.ebm',string='Customer ID')

    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['user.ebm'].search([])[-1].user_id)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a.replace("UR",""))
            a=str(a+1)
        if len(a)==1:
            a="0"+a
        for rec in vals:
            rec.update(
                {
                 'user_id': "UR" + a
                 }
            )
        return super(UserEBM, self).create(vals)

    @api.constrains('email')
    def _check_email(self):
        email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        for record in self:
            if record.email and not re.match(email_pattern, record.email):
                raise ValidationError("The email address '%s' is not valid." % record.email)

    @api.constrains('phone')
    def _check_phone(self):
        phone_pattern = r"(^[6-9]\d{9})"
        for record in self:
            if record.phone and not re.match(phone_pattern, record.phone):
                raise ValidationError("The phone number'%s' is not valid." % record.phone)
