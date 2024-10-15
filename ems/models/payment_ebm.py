from odoo import api, fields, models
from datetime import datetime


class PaymentEBM(models.Model):
    _name = 'payment.ebm'
    _description = 'Payment Details'
    _rec_name = 'payment_id'

    payment_id = fields.Char(string='Reference Number', readonly=True)
    payment_date = fields.Date(string='Payment Date', default=fields.Date.today())
    amount = fields.Float(string='Amount',compute='_compute_amount',store=True)
    invoice_id = fields.Many2one("invoice.ebm",string="Invoice")
  
    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['payment.ebm'].search([])[-1].payment_id)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a.replace("PAY",""))
            a=str(a+1)
        if len(a)==3:
            a="0"+a
        elif len(a)==2:
            a="00"+a
        elif len(a)==1:
            a="000"+a
        for rec in vals:
            z = self.env['invoice.ebm'].search([('id','=',rec['invoice_id'])])
            z.status = 'Paid'
            rec.update(
                {
                 'payment_id': "PAY" + a,
                 }
            )
        return super(PaymentEBM, self).create(vals)

    @api.depends('invoice_id')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.invoice_id.total_amount
