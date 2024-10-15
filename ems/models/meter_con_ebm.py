from odoo import api, fields, models


class MeterConnectionEBM(models.Model):
    _name = 'meter.con.ebm'
    _description = 'Meter Connection'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    desc = fields.Text(string='Description')