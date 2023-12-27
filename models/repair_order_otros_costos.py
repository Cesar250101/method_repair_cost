# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OtrosCostosRMA(models.Model):
    _name = 'method_repair_cost.otros_costo_rma'
    _description = 'Otros costos asociados a las RMA'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Empleado',domain = "[('costeo_rma','!=',True)]")
    cantidad = fields.Float(string='Cantidad de Horas')
    precio = fields.Integer(string='Costo por Hora')
    total = fields.Integer(compute='_compute_costo_total_hora', string='SubTotal',store=True)
    repair_id = fields.Many2one(comodel_name='repair.order',string= 'Orden de Reparaciòn',
                                index=True, ondelete='cascade', required=True)
    fecha = fields.Date(string='Fecha')
    tipo =fields.Selection([('combustible','Combustible'),
                            ('alojamiento','Alojamiento'),
                            ('viatico','Viatico'),
                            ('ss_interno','Servicios Internos'),],string='Tipo Gasto')
    factor_hh = fields.Float(string='Factor HH', default=1.4)
    obs = fields.Char(string='Descripción')
    

    @api.one
    @api.depends('employee_id','cantidad','precio')
    def _compute_costo_total_hora(self):
        if self.cantidad and self.precio:
            subtotal=round(float(self.cantidad)*float(self.precio))
            self.total=subtotal
            return self.total
