from odoo import api, fields, models
from datetime import datetime


class MeterEBM(models.Model):
    _name = 'meter.ebm'
    _description = 'Meter'
    _rec_name = 'meter_num'

    meter_num = fields.Char(string='Meter Number', readonly=True, size=12)
    customer_id = fields.Many2one('customer.ebm',string='Customer ID')
    meter_type = fields.Many2one('meter.type.ebm',string='Meter Type')
    meter_con = fields.Many2one('meter.con.ebm',string='Connection Type')
    instl_date = fields.Date(string='Installation Date', default=fields.Date.today())
    meter_desc = fields.Text(related='meter_type.desc',string='Meter Desc')
    con_desc = fields.Text(related='meter_con.desc',string='Connection Desc')
    reading_ids = fields.One2many('reading.ebm','meter_id',string='Readings')

    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['meter.ebm'].search([])[-1].meter_num)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a[7:])
            a=str(a+1)
        if len(a)==3:
            a="0"+a
        elif len(a)==2:
            a="00"+a
        elif len(a)==1:
            a="000"+a
        for rec in vals:
            b = self.env['customer.ebm'].search([('id','=',rec['customer_id'])])
            z1 = (b.pincode_id.city_id.district_id.uq_code)
            z2 = (b.pincode_id.city_id.uq_code)
            z3 = (b.pincode_id.uq_code)
            c = z1 + z2 + z3
            rec.update(
                {
                 'meter_num': c+str(a),
                 }
            )
        return super(MeterEBM, self).create(vals)

    def nav_meter(self):
        for i in self:
            return {
                'name': 'Meter',
                'type': 'ir.actions.act_window',
                'res_id': i.id,
                'view_mode': 'form',
                'res_model': 'meter.ebm',
            }