from odoo import api,fields,models

class ReportInvoiceEBMab(models.AbstractModel):
    _name = 'report.ebm.invoice_report_template'
    _description = 'Report_Invoice_EBM'

    def _get_report_values(self,docids, data):
        f_date = data['date_from']
        t_date = data['date_to']
        status = data['status']
        a1 = data['from']
        a2 = data['to']
        if status == "All":
            invoice_records = self.env['invoice.ebm'].search([('invoice_date', '>=', f_date),('invoice_date', '<=', t_date)])
        else:
            invoice_records = self.env['invoice.ebm'].search([('invoice_date', '>=', f_date),('invoice_date', '<=', t_date),('status', '=', status)])
        return {
            'doc_ids': self.ids,
            'invoice_records': invoice_records,
            'from': a1,
            'to': a2,
        }

class ReportDueDateEBMab(models.AbstractModel):
    _name = 'report.ebm.duedate_report_template'
    _description = 'Report_DueDate_EBM'

    def _get_report_values(self,docids, data):
        f_date = data['date_from']
        t_date = data['date_to']
        status = data['status']
        a1 = data['from']
        a2 = data['to']
        if status == "All":
            invoice_records = self.env['invoice.ebm'].search([('invoice_date', '>=', f_date),('invoice_date', '<=', t_date)])
        else:
            invoice_records = self.env['invoice.ebm'].search([('invoice_date', '>=', f_date),('invoice_date', '<=', t_date),('status', '=', status)])
        return {
            'doc_ids': self.ids,
            'invoice_records': invoice_records,
            'from': a1,
            'to': a2,
        }
