from openerp import models, fields, api,_


# Customer Invoice Model start

class CustomerInvoiceModel(models.Model):

    _inherit = 'account.invoice'
    _name = 'account.invoice'

    testField = fields.Char(string='testField')

# Customer Invoice Model end