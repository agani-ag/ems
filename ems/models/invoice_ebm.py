from odoo import api, fields, models
from datetime import datetime,date
import calendar


class InvoiceEBM(models.Model):
    _name = 'invoice.ebm'
    _description = 'Invoice Details'
    _rec_name = 'invoice_id'

    invoice_id = fields.Char(string='Invoice Number', readonly=True)
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.today())
    due_date = fields.Date(string='Due Date',)
    customer_id = fields.Many2one("customer.ebm",string="Customer")
    meter_id = fields.Many2one("meter.ebm",string="Meter")
    tariff_id = fields.Many2one("tariff.ebm",string="Tariff")
    payment_ids = fields.One2many("payment.ebm","invoice_id",string="Payment")
    exist_inv_id = fields.Char(string='EII', readonly=True)
    amount = fields.Float(string='Amount')
    due_amount = fields.Float(string='Due Amount')
    total_amount = fields.Float(string='Total Amount',compute='_compute_total',store=True)
    status  = fields.Selection([
            ('Not Paid', 'Not Paid'),
            ('Paid', 'Paid'),
            ('On Due', 'On Due'),
        ], string="Status" ,default='Not Paid')


    @api.model_create_multi
    def create(self, vals):
        try:
            a=str(self.env['invoice.ebm'].search([])[-1].invoice_id)
        except IndexError:
            a="1"
        if a != "1":
            a=int(a.replace("REF",""))
            a=str(a+1)
        if len(a)==3:
            a="0"+a
        elif len(a)==2:
            a="00"+a
        elif len(a)==1:
            a="000"+a
        for rec in vals:
            rec.update(
                {
                 'invoice_id': "REF" + a,
                 }
            )
        return super(InvoiceEBM, self).create(vals)

    @api.model
    def default_get(self, vals):
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        last_day = calendar.monthrange(current_year, current_month)[1]
        a = date(current_year, current_month, last_day)
        res = super(InvoiceEBM, self).default_get(vals)
        res.update({'due_date': a})
        return res

    @api.depends("customer_id")
    def _compute_total(self):
        for rec in self:
            rec.total_amount = rec.amount + rec.due_amount

    def _due_update(self):
        today = datetime.now().date()
        invoices = self.env['invoice.ebm'].search([])
        for rec in invoices:
            if rec.status == 'Not Paid':
                if rec.due_date < today:
                    rec.status = "On Due"
                    rec.due_amount = rec.due_amount + rec.tariff_id.due_price
            elif rec.status == 'On Due':
                rec.due_amount = rec.due_amount + rec.tariff_id.due_price

    def due_update_bt(self):
        today = datetime.now().date()
        for rec in self:
            if rec.status == 'Not Paid':
                if rec.due_date < today:
                    rec.status = "On Due"
                    rec.due_amount = rec.due_amount + rec.tariff_id.due_price
            elif rec.status == 'On Due':
                rec.due_amount = rec.due_amount + rec.tariff_id.due_price

    def invoice_print(self):
        return self.env.ref('ebm.invoice_ebm_report').report_action(self)