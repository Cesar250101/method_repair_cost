# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Facturas(models.Model):
    _inherit = 'account.invoice'

    repair_id = fields.Many2one(comodel_name='repair.order', string='Orden de Reparaciòn',
                                domain="[('state', 'in', ['confirmed','under_repair','ready','2binvoiced','invoice_except'])]")
    rma_lines = fields.Boolean(string='Habilitar RMA en Líneas')

class LineasFacturs(models.Model):
    _inherit = 'account.invoice.line'
   
    repair_id = fields.Many2one(comodel_name='repair.order', string='Orden de Reparaciòn',
                                domain="[('state', 'in', ['confirmed','under_repair','ready','2binvoiced','invoice_except'])]")