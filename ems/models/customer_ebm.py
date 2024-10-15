from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class CustomerEBM(models.Model):
    _name = 'customer.ebm'
    _description = 'Customer'
    _rec_name = 'name'

    customer_id = fields.Char(string='Customer ID', readonly=True)
    name = fields.Char(string='Name',required=True)
    phone = fields.Char(string="Phone", size=10)
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    pincode_id = fields.Many2one('pincode.ebm',string='Pin Code')
    pin_code = fields.Char(related='pincode_id.code',string='Pin Code',store=True)
    village = fields.Char(related='pincode_id.name',string='Village',store=True)
    city_id = fields.Char(related='pincode_id.city_id.name',string='City',store=True)
    district_id = fields.Char(related='pincode_id.city_id.district_id.name',string='District',store=True)
    meter_ids = fields.One2many('meter.ebm','customer_id',string='Meter')
    user_ids = fields.One2many('user.ebm','customer_id',string='User')

    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['customer.ebm'].search([])[-1].customer_id)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a.replace("CUS",""))
            a=str(a+1)
        if len(a)==1:
            a="0"+a
        for rec in vals:
            rec.update(
                {
                 'customer_id': "CUS" + a
                 }
            )
        return super(CustomerEBM, self).create(vals)

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
