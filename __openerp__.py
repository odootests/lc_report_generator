# -*- coding: utf-8 -*-
{
    'name' : 'LC Report Generator',

    'summary': "LC report management",

    'description': 'Simplly creat your LC report',

    'author': "Arnav, Metaporphosis.com.bd",
    'website': "http://www.metamorphosis.com.bd/",

    'version': '0.1',

    'depends': [
        'base',
        'account',
    ],

    'data': [ 
        'views/customer_invoices_records.xml',
        'views/commercial_invoices.xml',
        'views/lc_informations.xml',
        'views/invoice_name_sequence.xml',
        'views/country_origin.xml', 
        'views/delivery_transport.xml',
        'views/delivery_address.xml', 
        'views/shipping_factory_name_address.xml',
    ],
    'auto_install':False,
    'installable': True,
}    