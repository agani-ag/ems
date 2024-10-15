from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class CityEBM(models.Model):
    _name = 'city.ebm'
    _description = 'City Details'
    _rec_name = 'name'

    city_id = fields.Char(string="City ID", readonly=True)
    name = fields.Char(string='Name')
    district_id = fields.Many2one('district.ebm',string="District")
    pincode_ids = fields.One2many('pincode.ebm','city_id',string='Pincode')
    uq_code = fields.Char(string="Unique ID", readonly=True)

    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['city.ebm'].search([])[-1].city_id)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a.replace("CTY",""))
            a=str(a+1)
        if len(a)==1:
            b="43"+a
            a="0"+a
        for rec in vals:
            rec.update(
                {
                 'city_id': "CTY" + a,
                 'uq_code': b
                 }
            )
        return super(CityEBM, self).create(vals)
