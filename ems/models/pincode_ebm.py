from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class PinCodeEBM(models.Model):
    _name = 'pincode.ebm'
    _description = 'Pincode Details'
    _rec_name = 'code'

    code = fields.Char(string='Pin Code', readonly=True, size=6)
    name = fields.Char(string='Name')
    city_id = fields.Many2one('city.ebm',string='City')
    uq_code = fields.Char(string="Unique ID", readonly=True)
    

    @api.model_create_multi
    def create(self, vals):
        try:
            a=int(self.env['pincode.ebm'].search([])[-1].code)
            b=int(self.env['pincode.ebm'].search([])[-1].uq_code)
        except IndexError:
            a=635850
            b="1"
        if b != "1":
            b=int(b)
            b=str(b+1)
        if len(b)==1:
            b="0"+b
        a = a + 1
        for rec in vals:
            rec.update(
                {
                 'code': str(a),
                 'uq_code': b
                 }
            )
        return super(PinCodeEBM, self).create(vals)
