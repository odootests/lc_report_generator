from openerp import models, fields, api,_
# from openerp.exceptions import ValidationError

# commercial invoice Model start

class CommercialInvoiceModel(models.Model):
    _name = 'commercial_invoice.model'

    # _rec_name = "reservation_no"
    _rec_name = "name"

    name = fields.Char(string='Commercial Invoice Number', size=100, readonly=True)
    commercial_invoice_created_date = fields.Date(string='Date', readonly=True, default=fields.Datetime.now, required=True)

    # reservation_no = fields.Char('Reservation No', size=64, readonly=True)
    # reservation_no2 = fields.Char('Reservation No', size=64, readonly=True)

    account_invoice_id = fields.Many2one('account.invoice',string='Porforma Invoice No.', required=True)
    account_invoice_id2 = fields.Char(string='account_invoice_id')
    invoice_created_date = fields.Date(string='Invoice Date')

    customer_name = fields.Char(string='Customer Name', size=250)
    customer_name2 = fields.Char(string='Customer Name', size=250)
    customer_full_address = fields.Text(string='Customer Address')

    country_of_origin = fields.Many2one('country_origin.model',string='Country Of Origin', required=True)
    country_of_origin2 = fields.Char(string='Country Of Origin')

    destination_address = fields.Text(string='Destination')

    
    transport = fields.Many2one('delivery_transport.model',string='Means of Transport', required=True)
    dealer_factory_name = fields.Many2one('delivery_address.model',string='Delivery From', required=True)
    beneficiary_vat_no = fields.Char(string='Beneficiary Vat No:', size=100)
    hs_Code = fields.Char(string='HS Code', size=100)
    erc_no = fields.Char(string='ERC No', size=100)

    client_shipping_factory_name = fields.Many2one('shipping_factory_name_address.model',string='Factory Name', required=True)
    client_shipping_factory_address = fields.Text(string='Factory Address')

    lc_num = fields.Many2one('lc_informations.model','L/C No.', required=True)
    lc_num2 = fields.Char(string='L/C No.',size=64)
    lc_date = fields.Date(string='L/C Dated')
    lc_date2 = fields.Date(string='L/C Dated')
    
    issuing_bank = fields.Text(string='Issuing Bank')
    vat_code = fields.Text(string='VAT Reg./H.S Code')
    irc_num = fields.Text(string='IRC/TIN/BIN No.')
    sales_contact_num = fields.Text(string='Sales Contact no.')
    sales_contact_date = fields.Date(string='Sales Contact date')

    ordered_products_name = fields.Text(string='ordered_products_name') 
    ordered_products_number_of_bags = fields.Text(string='ordered_products_number_of_bags') 
    ordered_products_quantity = fields.Text(string='ordered_products_quantity') 
    ordered_products_price_of_unit = fields.Text(string='ordered_products_price_of_unit')
    ordered_products_amount = fields.Text(string='ordered_products_amount')

    ordered_products_total_quantity = fields.Char(string='ordered_products_total_quantity')
    ordered_products_total_amount = fields.Char(string='ordered_products_total_amount')

    currency_symbol = fields.Char(string='currency_symbol')
    currency_symbol1 = fields.Char(string='currency_symbol')

    #This fuction is for create a uniq number for a invoice report.
    @api.model
    def create(self, vals):
        """
        Overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        if not vals:
            vals = {}
        seq_obj = self.env['ir.sequence']
        invoice_num = seq_obj.next_by_code('commercial_invoices.model') or 'New'
        vals['name'] = invoice_num
        return super(CommercialInvoiceModel, self).create(vals)

  

    # This function is for load data automatically in the existing field from another table
    def onchange_lc_num_service(self, cr, uid, ids, lc_num=False, context=None):
        res= {}
        if lc_num:
            service_obj= self.pool.get('lc_informations.model')
            rec = service_obj.browse(cr, uid, lc_num)
            bank_info = str(rec.lc_bank_name) + "\n\n" + str(rec.lc_bank_branch) + "\n" + str(rec.lc_bank_address)
            res= {'value':{'lc_date':rec.lc_date,'issuing_bank':bank_info, 'lc_num2':rec.name, 'lc_date2':rec.lc_date}}
        else:
            res= {'value':{'lc_date':False,'issuing_bank':False}}
        return res

    # This function is for load data automatically in the existing field from another table   
    def onchange_account_invoice_id(self, cr, uid, ids, account_invoice_id=False, context=None):
        res= {}
        if account_invoice_id:

            service_obj= self.pool.get('account.invoice').browse(cr, uid,account_invoice_id,context=context)
            service_obj2= self.pool.get('res.partner').browse(cr, uid,service_obj.partner_id.id,context=context)
            service_obj3= self.pool.get('res.country').browse(cr, uid,service_obj2.country_id.id,context=context)
            currency_symbol= self.pool.get('res.currency').browse(cr, uid,service_obj.currency_id.id,context=context)
            
            cus_full_address = str(service_obj2.street) + " , " + str(service_obj2.street2) + " , " + str(service_obj2.city)+ " - " + str(service_obj2.zip) + " , " + str(service_obj3.name)




            invoice_line_pool_ids = self.pool.get('account.invoice.line').search(cr, uid,[('invoice_id','=',account_invoice_id),],context=context)

            invoice_lines_product_name = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['name'], context=context)

            invoice_lines_product_quantity = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['quantity'], context=context)

            invoice_lines_product_price_of_unit = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_unit'], context=context)

            invoice_lines_product_amount = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['price_subtotal'], context=context)

            # invoice_lines_product_amount_currency = self.pool.get('account.invoice.line').read(cr, uid,invoice_line_pool_ids,['currency_id'], context=context)
            


            ordered_products_names = self.split_products_names(invoice_lines_product_name) 

            ordered_products_number_of_bags = self.split_products_number_of_bags(invoice_lines_product_quantity)

            ordered_products_quantity = self.split_products_quantity(invoice_lines_product_quantity)

            ordered_products_price_of_unit = self.split_products_price_of_unit(invoice_lines_product_price_of_unit)

            ordered_products_amount = self.split_products_amount(invoice_lines_product_amount)

            ordered_products_total_quantity = self.products_total_quantity(invoice_lines_product_quantity)

            ordered_products_total_amount = self.products_total_amount(invoice_lines_product_amount)

            # currency_symbol = self.get_currency(invoice_lines_product_amount_currency)



            res = {'value':{'account_invoice_id2':service_obj.number,'invoice_created_date':service_obj.date_invoice,'customer_name':service_obj2.name,'customer_name2':service_obj2.name,'customer_full_address':cus_full_address,'ordered_products_name':ordered_products_names,'ordered_products_number_of_bags':ordered_products_number_of_bags, 'ordered_products_quantity':ordered_products_quantity,'ordered_products_price_of_unit':ordered_products_price_of_unit,'ordered_products_amount':ordered_products_amount,'ordered_products_total_quantity':ordered_products_total_quantity,'ordered_products_total_amount':ordered_products_total_amount,
            'currency_symbol':currency_symbol.symbol,
            'currency_symbol1':currency_symbol.symbol
            }}
             

        else:
            res={}  
        return res    

    def split_products_names(self,invoice_lines_product_name):
        names= []
        idx = 0
        for r in invoice_lines_product_name:
            names.append(r['name'])
            combine = '\n \n'.join([str(i) for i in names])  
        return combine

    def split_products_number_of_bags(self,invoice_lines_product_quantity):
        number_of_bags= []
        idx = 0
        for r in invoice_lines_product_quantity:
            number_of_bags.append(int(r['quantity'] / 50))
            combine = '\n \n \n'.join([str(i) for i in number_of_bags])
        return combine

    def split_products_quantity(self,invoice_lines_product_quantity):
        quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            quantity.append(int(r['quantity']))
            combine = '\n \n \n'.join([str(i) for i in quantity])
        return combine

    def split_products_price_of_unit(self,invoice_lines_product_price_of_unit):
        price_of_unit= []
        idx = 0
        for r in invoice_lines_product_price_of_unit:
            price_of_unit.append(r['price_unit'])
            combine = '\n \n \n'.join([str(i) for i in price_of_unit])
        return combine

    def split_products_amount(self,invoice_lines_product_amount):
        amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            amount.append(r['price_subtotal'])
            combine = '\n \n \n'.join([str(i) for i in amount])
        return combine

    def products_total_quantity(self,invoice_lines_product_quantity):
        total_quantity= []
        idx = 0
        for r in invoice_lines_product_quantity:
            total_quantity.append(r['quantity'])
            in_com = sum(total_quantity)
            combine = int(in_com)
        return combine   

    def products_total_amount(self,invoice_lines_product_amount):
        total_amount= []
        idx = 0
        for r in invoice_lines_product_amount:
            total_amount.append(r['price_subtotal'])
            combine = sum(total_amount)
        return combine



      
    def onchange_country_origin(self, cr, uid, ids, country_of_origin=False, context=None):
        res= {}
        if country_of_origin:
            service_obj= self.pool.get('country_origin.model')
            rec = service_obj.browse(cr, uid, country_of_origin)
            res = {'value':{'country_of_origin2':rec.name}}
        else:
            res={}  
        return res

    def onchange_client_shipping_factory_name(self, cr, uid, ids, client_shipping_factory_name=False, context=None):
        res= {}
        if client_shipping_factory_name:
            service_obj= self.pool.get('shipping_factory_name_address.model')
            rec = service_obj.browse(cr, uid, client_shipping_factory_name)
            res = {'value':{'client_shipping_factory_address':rec.address}}
        else:
            res={}  
        return res









