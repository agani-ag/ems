from odoo import api, fields, models
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
import calendar

class WizardInvoiceEBMReport(models.TransientModel):
    _name = 'wizard.invoice.ebm.report'
    _description = 'WizardInvoiceEBMReport'

    date_from = fields.Date(string="From")
    date_to = fields.Date(string="To", default=fields.Date.today())
    report_sel  = fields.Selection([
            ('Current Month', 'Current Month'),
            ('Last Month', 'Last Month'),
            ('Custom Dates', 'Custom Dates'),
        ], string="Report Type" ,default='Current Month')
    status  = fields.Selection([
            ('All', 'All'),
            ('Not Paid', 'Not Paid'),
            ('Paid', 'Paid'),
            ('On Due', 'On Due'),
        ], string="Status" ,default='All')


    def invoice_report_pdf(self):
        now = datetime.now().date()
        data = {}
        if self.report_sel == "Custom Dates":
            data['date_from'] = self.date_from
            data['date_to'] = self.date_to
            data['status'] = self.status
            data['from'] = self.date_from.strftime('%d-%m-%Y')
            data['to'] = self.date_to.strftime('%d-%m-%Y')
        elif self.report_sel == "Last Month":
            data['date_from'] = (now - relativedelta(months=1)).replace(day=1)
            data['date_to'] = (now - relativedelta(months=1)).replace(day=30)
            data['status'] = self.status
            data['from'] = self.date_from.strftime('%d-%m-%Y')
            data['to'] = self.date_to.strftime('%d-%m-%Y')
        else:
            data['date_from'] = date(now.year, now.month, 1)
            data['date_to'] = now
            data['status'] = self.status
            data['from'] = self.date_from.strftime('%d-%m-%Y')
            data['to'] = self.date_to.strftime('%d-%m-%Y')
        if self.status == "On Due":
            return self.env.ref('ebm.duedate_ebm_report_action').report_action(self, data=data)
        return self.env.ref('ebm.invoice_ebm_report_action').report_action(self, data=data)

    @api.model
    def default_get(self, vals):
        now = datetime.now()
        a = date(now.year, now.month, 1)
        res = super(WizardInvoiceEBMReport, self).default_get(vals)
        res.update({'date_from': a})
        return res 


