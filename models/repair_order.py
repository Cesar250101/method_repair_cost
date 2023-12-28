# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Rma(models.Model):
    _inherit = 'repair.order'

    costeo_inventario = fields.Integer(string='Costeo Salidas Inventario',compute='_compute_costeo_inventario',store=True)
    costeo_inventario_porc = fields.Float(string='% Costeo Salidas Inventario',compute='_compute_costeo_inventario',store=True)
    costeo_facturas = fields.Integer(string='Costeo Facturas de Compra',compute='_compute_costeo_facturas',store=True)
    costeo_facturas_porc = fields.Float(string='% Costeo Facturas Compra',compute='_compute_costeo_facturas',store=True)    
    costeo_hh = fields.Integer(string='Costeo Horas Hombre',compute='_compute_costeo_hh',store=True)
    costeo_hh_porc = fields.Float(string='% Costeo Horas Hombre',compute='_compute_costeo_hh',store=True)        
    costeo_hh_normal = fields.Integer(string='Costeo Horas Normal',compute='_compute_costeo_hh',store=True)
    costeo_hh_normal_porc = fields.Float(string='% Costeo Horas Hombre',compute='_compute_costeo_hh',store=True)            
    costeo_hh_50 = fields.Integer(string='Costeo Horas 50%',compute='_compute_costeo_hh',store=True)
    costeo_hh_50_porc = fields.Float(string='% Costeo Horas Hombre',compute='_compute_costeo_hh',store=True)                
    costeo_hh_100 = fields.Integer(string='Costeo Horas H100%',compute='_compute_costeo_hh',store=True)
    costeo_hh_100_porc = fields.Float(string='% Costeo Horas Hombre',compute='_compute_costeo_hh',store=True)                    
    costeo_otros = fields.Integer(string='Costeo Otros',compute='_compute_costeo_otros',store=True)
    costeo_otros_porc = fields.Float(string='% Costeo Horas Hombre',compute='_compute_costeo_otros',store=True)                        
    costeo_hh_ids = fields.One2many(comodel_name='method_repair_cost.costo_hh',inverse_name= 'repair_id', string='Costeo HH',
                                    copy=True, readonly=True, states={'draft': [('readonly', False)]})
    picking_ids = fields.One2many(comodel_name='stock.picking', inverse_name= 'repair_id', string='Salidas Inventario')
    invoice_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='repair_id', string='Facturas')
    total_costo = fields.Integer(string='Costo Total',compute='_compute_total_costo',store=True)
    total_costo_porc = fields.Float(string='% Costeo Horas Hombre',compute='_compute_total_costo',store=True)                            
    margen = fields.Integer(string='Margen',compute='_compute_total_costo',store=True)
    margen_porc = fields.Float(string='% Costeo Horas Hombre',compute='_compute_total_costo',store=True)                                
    otros_costos_ids = fields.One2many(comodel_name='method_repair_cost.otros_costo_rma',inverse_name= 'repair_id', string='Otros Costos',
        copy=True, readonly=True, states={'draft': [('readonly', False)]})
    categ_texto_costo = fields.Text(string='Apertura costeo inventario',compute='_compute_costeo_inventario',store=True)


    @api.depends('costeo_hh_ids','picking_ids','invoice_ids','amount_untaxed')
    def _compute_margen(self):
        self.margen=self.amount_untaxed-self.total_costo  

    @api.one
    @api.depends('costeo_hh_ids','picking_ids','invoice_ids','otros_costos_ids')
    def _compute_total_costo(self):
        total_costo=self.costeo_facturas+self.costeo_hh+self.costeo_inventario+self.costeo_otros
        self.total_costo=total_costo
        self.margen=self.amount_untaxed-total_costo
        try:
            self.total_costo_porc=round(((total_costo/self.amount_untaxed)*100),2)
            self.margen_porc=round(((self.margen/self.amount_untaxed)*100),2)
        except:
            pass

    @api.one
    @api.depends('costeo_hh_ids','amount_untaxed')
    def _compute_costeo_hh(self):
        costo_hh=0
        costo_hh_normal=0
        costo_hh_50=0
        costo_hh_100=0

        costo_hh_porc=0
        costo_hh_normal_porc=0
        costo_hh_50_porc=0
        costo_hh_100_porc=0

        for i in self.costeo_hh_ids:
            costo_hh+=i.costo_total_hora    
            if i.tipo=="normal":
                costo_hh_normal+=i.costo_total_hora
            elif i.tipo=="50":
                costo_hh_50+=i.costo_total_hora
            elif i.tipo=="100":
                costo_hh_100+=i.costo_total_hora                
        self.costeo_hh=costo_hh
        self.costeo_hh_normal=costo_hh_normal
        self.costeo_hh_50=costo_hh_50
        self.costeo_hh_100=costo_hh_100
        self.total_costo=self.costeo_hh+self.costeo_inventario+self.costeo_facturas
        self.margen=self.amount_untaxed-self.total_costo

        try:
            costo_hh_porc=round((costo_hh/self.amount_untaxed)*100,2)
            costo_hh_normal_porc=round((costo_hh_normal/self.amount_untaxed)*100,2)
            costo_hh_50_porc=round((costo_hh_50/self.amount_untaxed)*100,2)
            costo_hh_100_porc=round((costo_hh_100/self.amount_untaxed)*100,2)

            self.costeo_hh_porc=costo_hh_porc
            self.costeo_hh_normal_porc=costo_hh_normal_porc
            self.costeo_hh_50_porc=costo_hh_50_porc
            self.costeo_hh_100_porc=costo_hh_100_porc


            self.total_costo_porc=round((self.total_costo/self.amount_untaxed)*100,2)
            self.margen_porc=round((self.margen/self.amount_untaxed)*100,2)
        except:
            pass

    @api.one
    @api.depends('otros_costos_ids','amount_untaxed')
    def _compute_costeo_otros(self):
        costo_hh=0
        for i in self.otros_costos_ids:
            costo_hh+=i.total    
        self.costeo_otros=costo_hh
        try:
            self.costeo_otros_porc=round(((costo_hh/self.amount_untaxed)*100),2)
        except:
            pass
        self.total_costo=self.costeo_hh+self.costeo_inventario+self.costeo_facturas+self.costeo_otros
        self.margen=self.amount_untaxed-self.total_costo        

    @api.one
    @api.depends('picking_ids','amount_untaxed')
    def _compute_costeo_inventario(self):
        costo_inventario=0
        costo_inventario_porc=0.00
        for i in self.picking_ids:
            for l in i.move_ids_without_package:
                costo_inventario+=l.product_qty*l.product_id.standard_price
        self.costeo_inventario=costo_inventario
        try:
            costo_inventario_porc=(costo_inventario/self.amount_untaxed)*100
            self.costeo_inventario_porc=costo_inventario_porc
        except:
            pass
        self.total_costo=self.costeo_hh+self.costeo_inventario+self.costeo_facturas+self.costeo_otros
        self.margen=self.amount_untaxed-self.total_costo
        if self.id:
            sql="""
                select pc.name Categoria,coalesce(sum(sm.product_qty*(select cost from product_price_history pph 
                                                                where pph.product_id=pp.id
                                                                order by datetime desc  limit 1)),0) costo
                from stock_picking sp,stock_move sm,product_product pp,product_template pt,product_category pc  
                where sp.repair_id ={}
                and sp.id =sm.picking_id 
                and sm.product_id =pp.id 
                and pp.product_tmpl_id =pt.id 
                and pt.categ_id =pc.id 
                group by pc.name

                """.format(self.id)
            self.env.cr.execute(sql)
            datos=self.env.cr.fetchall()
            texto=""
            for dato in datos:
                texto+=dato[0] +" : "+str(dato[1])+"\n"
            self.categ_texto_costo=texto




    @api.one
    @api.depends('invoice_ids','amount_untaxed')
    def _compute_costeo_facturas(self):
        costo_facturas=0
        costo_facturas_porc=0.00
        for i in self.invoice_ids:
            costo_facturas+=i.price_subtotal
        self.costeo_facturas=costo_facturas
        try:
            costo_facturas_porc=round((costo_facturas/self.amount_untaxed)*100,2)
            self.costeo_facturas_porc=costo_facturas_porc
        except:
            pass
        self.total_costo=self.costeo_hh+self.costeo_inventario+self.costeo_facturas
        self.margen=self.amount_untaxed-self.total_costo


class CosteHH(models.Model):
    _name = 'method_repair_cost.costo_hh'
    _description = 'Horas trabajadas por empleado'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Empleado',domain = "[('costeo_rma','!=',True)]")
    cantidad_hh = fields.Float(string='Cantidad de Horas')
    costo_hora = fields.Integer(compute='_compute_costo_hora', string='Costo por Hora',store=True)
    costo_total_hora = fields.Integer(compute='_compute_costo_total_hora', string='Costo por Hora',store=True)
    repair_id = fields.Many2one(comodel_name='repair.order',string= 'Orden de Reparaciòn',
                                index=True, ondelete='cascade', required=True)
    fecha_hh = fields.Date(string='Fecha')
    tipo =fields.Selection([('normal','Normal X Factor'),
                            ('50','HH Extra 50%'),
                            ('100','HH Extra 100%')],string='Tipo')
    factor_hh = fields.Float(string='Factor HH', default=1.4)
    obs = fields.Char(string='Descripción')
    

    @api.one
    @api.depends('employee_id','cantidad_hh','costo_hora','factor_hh')
    def _compute_costo_total_hora(self):
        if self.cantidad_hh and self.costo_hora:
            subtotal=round(float(self.cantidad_hh)*float(self.costo_hora)*float(self.factor_hh if self.tipo=='normal' else 1))
            self.costo_total_hora=subtotal
            return self.costo_total_hora
    @api.one
    @api.depends('employee_id','tipo')
    def _compute_costo_hora(self):
        if self.employee_id:
            total_haberes_id=self.env['hr.salary.rule'].search([('code','=','SUELDO')],limit=1).id            
            nomina_id=self.env['hr.payslip'].search([('employee_id','=',self.employee_id.id)],order="id desc",limit=1)
            domain=[
                    ('salary_rule_id','=',total_haberes_id),
                    ('slip_id','=',nomina_id.id),
                    ('employee_id','=',self.employee_id.id)
                ]            
            total_haberes=nomina_id.line_ids.search(domain,limit=1).amount            
            if self.tipo=='normal':
                #Ejemplo: sueldo de $400.000 / 30 X 28 /180= $2.074 cada hora ordinaria.
                valor_hora=((total_haberes/30)*28)/180                 
            elif self.tipo=='50':
                valor_hora=round(total_haberes*0.00777777)
            elif self.tipo=='100':
                valor_hora=round(total_haberes*0.0103704)
            self.costo_hora=round(valor_hora)           
            return self.costo_hora