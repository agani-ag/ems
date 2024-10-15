from odoo.http import request, route, Controller
from datetime import datetime


class EBMControllers(Controller):

    @route('/ebcheck', auth='public', type='http', website=True)
    def get_track(self):
        return request.render('ebm.meter_login')

    @route('/eb/invoice', auth='public', type='http', website=True)
    def get_track_booking(self,**kwargs):
        meter_number = kwargs.get('number')
        meter = request.env['meter.ebm'].search([('meter_num','=',meter_number)])
        meter_id = meter.id
        invoice = request.env['invoice.ebm'].search([('meter_id','=',meter_id)])[-1]
        return request.render('ebm.eb_invoice',{'invoice': invoice})
        


