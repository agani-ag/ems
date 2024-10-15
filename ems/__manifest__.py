# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Electricity Billing Management',
    'author' : 'Skynet AG Services',
    'license' : 'LGPL-3',
    'version': '1.0',
    'category': 'EB',
    'sequence': 225,
    'summary': 'EB Management',
    'depends': ['mail'],
    'data': [
        'security/ebm_security.xml',
        'security/ir.model.access.csv',
        'views/menu_ebm.xml',
        'views/customer_ebm.xml',
        'views/user_ebm.xml',
        'views/employee_ebm.xml',
        'views/district_ebm.xml',
        'views/city_ebm.xml',
        'views/pincode_ebm.xml',
        'views/meter_ebm.xml',
        'views/meter_type_ebm.xml',
        'views/meter_con_ebm.xml',
        'views/reading_ebm.xml',
        'views/tariff_ebm.xml',
        'views/invoice_ebm.xml',
        'views/payment_ebm.xml',
        'data/invoice_ebm_cron.xml',
        'data/invoice_ebm_ctrl.xml',
        'data/mail_invoice_ebm.xml',
        'wizard/wizard_invoice_ebm_report.xml',
        'views/report/invoice_date_report.xml',
        'views/report/duedate_report.xml',
        'views/report/invoice_report.xml',
        'views/res_users_inherit.xml',
        ],
    'installable': True,
    'application': True,
    'assets': {
    'web.assets_backend': [
        'ebm/static/src/css/ebm_styles.css',
    ],
},

}
