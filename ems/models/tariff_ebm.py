from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TariffEBM(models.Model):
    _name = 'tariff.ebm'
    _description = 'Tariff Details'
    _rec_name = "tariff_id"

    tariff_id = fields.Char(string="Tariff ID", readonly=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    end_date = fields.Date(string='End Date')
    dom_price = fields.Float(string='Domestic Price',required=True)
    com_price = fields.Float(string='Commercial Price',required=True)
    due_price = fields.Float(string='Due Price',required=True)

    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['tariff.ebm'].search([])[-1].tariff_id)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a.replace("TF",""))
            a=str(a+1)
        if len(a)==1:
            a="0"+a
        for rec in vals:
            rec.update(
                {
                 'tariff_id': "TF" + a
                 }
            )
        return super(TariffEBM, self).create(vals)

    @api.model
    def default_get(self, vals):
        a = datetime.today() + relativedelta(years=1)
        res = super(TariffEBM, self).default_get(vals)
        res.update({'end_date': a})
        return res  