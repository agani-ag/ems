from odoo import api, fields, models


class MeterTypeEBM(models.Model):
    _name = 'meter.type.ebm'
    _description = 'Meter Type'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    desc = fields.Text(string='Description')
    extra_price = fields.Float(string='Extra Price')