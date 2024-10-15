from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class DistrictEBM(models.Model):
    _name = 'district.ebm'
    _description = 'District Details'
    _rec_name = 'name'

    district_id = fields.Char(string="District ID", readonly=True)
    name = fields.Char(string='Name')
    state = fields.Char(string='State',default="Tamil Nadu")
    country = fields.Char(string='Country',default="India")
    uq_code = fields.Char(string="Unique ID", readonly=True)
    city_ids = fields.One2many('city.ebm','district_id',string='City')
    city_count = fields.Integer(string=": City Count", compute='_get_city_count')

    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['district.ebm'].search([])[-1].district_id)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a.replace("DST",""))
            a=str(a+1)
        if len(a)==1:
            a="0"+a
        for rec in vals:
            rec.update(
                {
                 'district_id': "DST" + a,
                 'uq_code'    : a
                 }
            )
        return super(DistrictEBM, self).create(vals)

    @api.depends('name')
    def _get_city_count(self):
        for rec in self:
            total = self.env['city.ebm'].search_count([('district_id','=',rec.id)])
            rec.city_count = total

    def nav_city(self):
        return {
            'name': 'Cities',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('district_id','=',self.id)],
            'res_model': 'city.ebm',
        }