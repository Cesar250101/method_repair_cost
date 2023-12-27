# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Rma(models.Model):
    _inherit = 'repair.order'

    costeo_inventario = fields.Integer(string='Costeo Salidas Inventario',compute='_compute_costeo_inventario')
    costeo_facturas = fields.Integer(string='Costeo Facturas de Compra',compute='_compute_costeo_facturas')
    costeo_hh = fields.Integer(string='Costeo Horas Hombre',compute='_compute_costeo_hh')
    costeo_otros = fields.Integer(string='Costeo Otros',compute='_compute_costeo_otros')
    costeo_hh_ids = fields.One2many(comodel_name='method_repair_cost.costo_hh',inverse_name= 'repair_id', string='Costeo HH',
                                    copy=True, readonly=True, states={'draft': [('readonly', False)]})
    picking_ids = fields.One2many(comodel_name='stock.picking', inverse_name= 'repair_id', string='Salidas Inventario')
    invoice_ids = fields.One2many(comodel_name='account.invoice.line', inverse_name='repair_id', string='Facturas')
    total_costo = fields.Integer(string='Costo Total',compute='_compute_total_costo',store=True)
    margen = fields.Integer(string='Margen',compute='_compute_total_costo',store=True)
    otros_costos_ids = fields.One2many(comodel_name='method_repair_cost.otros_costo_rma',inverse_name= 'repair_id', string='Otros Costos',
        copy=True, readonly=True, states={'draft': [('readonly', False)]})


    @api.depends('costeo_hh_ids','picking_ids','invoice_ids','amount_untaxed')
    def _compute_margen(self):
        self.margen=self.amount_untaxed-self.total_costo  

    @api.one
    @api.depends('costeo_hh_ids','picking_ids','invoice_ids','otros_costos_ids')
    def _compute_total_costo(self):
        total_costo=self.costeo_facturas+self.costeo_hh+self.costeo_inventario+self.costeo_otros
        self.total_costo=total_costo
        self.margen=self.amount_untaxed-total_costo

    @api.one
    @api.depends('costeo_hh_ids','amount_untaxed')
    def _compute_costeo_hh(self):
        costo_hh=0
        for i in self.costeo_hh_ids:
            costo_hh+=i.costo_total_hora    
        self.costeo_hh=costo_hh
        self.total_costo=self.costeo_hh+self.costeo_inventario+self.costeo_facturas
        self.margen=self.amount_untaxed-self.total_costo

    @api.one
    @api.depends('otros_costos_ids','amount_untaxed')
    def _compute_costeo_otros(self):
        costo_hh=0
        for i in self.otros_costos_ids:
            costo_hh+=i.total    
        self.costeo_otros=costo_hh
        self.total_costo=self.costeo_hh+self.costeo_inventario+self.costeo_facturas+self.costeo_otros
        self.margen=self.amount_untaxed-self.total_costo        

    @api.one
    @api.depends('picking_ids','amount_untaxed')
    def _compute_costeo_inventario(self):
        costo_inventario=0
        for i in self.picking_ids:
            for l in i.move_ids_without_package:
                costo_inventario+=l.product_qty*l.product_id.standard_price
        self.costeo_inventario=costo_inventario
        self.total_costo=self.costeo_hh+self.costeo_inventario+self.costeo_facturas
        self.margen=self.amount_untaxed-self.total_costo

    @api.one
    @api.depends('invoice_ids','amount_untaxed')
    def _compute_costeo_facturas(self):
        costo_facturas=0
        for i in self.invoice_ids:
            costo_facturas+=i.price_subtotal
        self.costeo_facturas=costo_facturas
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