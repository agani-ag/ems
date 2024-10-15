from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import ValidationError


class ReadingEBM(models.Model):
    _name = 'reading.ebm'
    _description = 'Meter Reading'
    _rec_name = 'reading_id'

    reading_id = fields.Char(string='Reading ID', readonly=True)
    reading_date = fields.Date(string='Reading Date', default=fields.Date.today())
    reading_value = fields.Integer(string='Reading Value' ,required=True)
    previous_value = fields.Integer(string='Previous Value' ,store=True)
    usage_value = fields.Integer(string='Usage Value' ,compute='_compute_usage_value',store=True)
    meter_id = fields.Many2one('meter.ebm',string='Meter',store=True)
    temp_meter_num = fields.Char(related='meter_id.meter_num',string='Meter Num')
    tariff_id = fields.Many2one('tariff.ebm',string='Tariff Plan')
    pay_amount = fields.Float(string='Amount',compute='_compute_pay_amount',store=True)

    @api.model_create_multi
    def create(self, vals):
        try:
            a = str(self.env['reading.ebm'].search([])[-1].reading_id) 
        except IndexError:
            a ="1"
        if a != "1":
            a=int(a.replace("RD",""))
            a=str(a+1)
        if len(a)==1:
            a="0"+a
        for rec in vals:
            rec.update(
                {
                 'reading_id': "RD" + a
                 }
            )
        return super(ReadingEBM, self).create(vals)

    @api.onchange('reading_date')
    def _compute_previous_value(self):
        for rec in self:
            j = self.env['meter.ebm'].search([('meter_num','=',rec.temp_meter_num)])
            meter_id = j.meter_num
            try:
                a = self.env['reading.ebm'].search([('meter_id','=',meter_id)])[-1].reading_value
            except IndexError:
                a = 0
            rec.previous_value = a

    @api.depends('reading_value')
    def _compute_usage_value(self):
        for rec in self:
            rec.usage_value = rec.reading_value - rec.previous_value

    @api.depends('usage_value')
    def _compute_pay_amount(self):
        for rec in self:
            type_per = rec.meter_id.meter_type.extra_price

            type = rec.meter_id.meter_type.name
            connect = rec.meter_id.meter_con.name
            units = rec.usage_value
            fixed_price_dom = rec.tariff_id.dom_price
            fixed_price_com = rec.tariff_id.com_price

            if connect == "Domestic":
                bill = self.domestic_eb_bill(units,fixed_price_dom,type,type_per)
            elif connect == "Commercial":
                bill = self.commercial_eb_bill(units,fixed_price_com,type,type_per)

            print(bill)

            rec.pay_amount = bill

    def domestic_eb_bill(self,units,fixed_price,type,type_per):
        if type == "Single Phase":
            a = fixed_price
            b = a + ( a * (25 / 100))
            c = b + ( b * (50 / 100))
        elif type == "Three Phase":
            a = fixed_price + (fixed_price * (type_per / 100))
            b = a + ( a * (25 / 100))
            c = b + ( b * (50 / 100))
        if units <= 100:
            bill = units * 0  # First 100 units
        elif units <= 200:
            bill = (100 * 0) + (units - 100) * a  # Next 100 units
        elif units <= 500:
            bill = (100 * 0) + (100 * a) + (units - 200) * b  # Next 300 units
        else:
            bill = (100 * 0) + (100 * a) + (300 * b) + (units - 500) * c  # Above 500 units
        
        return bill

    def commercial_eb_bill(self,units,fixed_price,type,type_per):
        if type == "Single Phase":
            a = fixed_price
            b = a + ( a * (25 / 100))
            c = b + ( b * (50 / 100))
            c = b + ( b * (75 / 100))
        elif type == "Three Phase":
            a = fixed_price + (fixed_price * (type_per / 100))
            b = a + ( a * (25 / 100))
            c = b + ( b * (50 / 100))
            d = c + ( c * (75 / 100))
        if units <= 100:
            bill = units * a  # First 100 units
        elif units <= 200:
            bill = (100 * a) + (units - 100) * a  # Next 100 units
        elif units <= 500:
            bill = (100 * a) + (100 * b) + (units - 200) * c  # Next 300 units
        else:
            bill = (100 * a) + (100 * b) + (300 * c) + (units - 500) * d  # Above 500 units
        
        return bill

    def update_invoice(self):
        for rec in self:
            eri = rec.reading_id + "INV"
            eri_rt = self.env['invoice.ebm'].search([('exist_inv_id', '=', eri)])
            if eri_rt:
                return {
                    'name': 'Invoice',
                    'type': 'ir.actions.act_window',
                    'res_id': eri_rt.id,
                    'view_mode': 'form',
                    'res_model': 'invoice.ebm',
                }
                # raise ValidationError('Already The Invoice Is Exist')
            else:
                if rec.pay_amount == 0:
                    invoice_bal = self.env['invoice.ebm'].create({
                    'amount': rec.pay_amount,
                    'customer_id': rec.meter_id.customer_id.id,
                    'meter_id': rec.meter_id.id,
                    'tariff_id': rec.tariff_id.id,
                    'status': "Paid",
                    'exist_inv_id': eri
                    })
                else:
                    invoice_bal = self.env['invoice.ebm'].create({
                        'amount': rec.pay_amount,
                        'customer_id': rec.meter_id.customer_id.id,
                        'meter_id': rec.meter_id.id,
                        'tariff_id': rec.tariff_id.id,
                        'exist_inv_id': eri
                    })
                template_id = self.env.ref('ebm.mail_invoice_ebm')
                template_id.send_mail(rec.id, force_send=True)
                return {
                            'effect': {
                                'fadeout': 'slow',
                                'message': "Invoice - Email Sent Successfully",
                                'type': 'rainbow_man',
                                'img_url':'ebm/static/img/like.png'
                            }
                        }
