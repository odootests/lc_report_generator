from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

class LCinformations(models.Model):
    _name = 'lc_informations.model'


    name = fields.Char(required=True, string='L/C No.',size=100)
    lc_date = fields.Date('L/C Created Dated', required=True, default=fields.Date.today())
    lc_bank_name = fields.Text('Bank Name')
    lc_bank_branch = fields.Text('Bank Brunch')
    lc_bank_address = fields.Text('Bank Address')


    @api.one 
    @api.constrains('lc_date')
    def _check_lc_date(self):
        if self.lc_date > fields.Date.today():
            raise ValidationError(_("L/C Date can't be greater than current date!"))