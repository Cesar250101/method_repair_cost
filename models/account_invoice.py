# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'account.invoice'

    repair_id = fields.Many2one(comodel_name='repair.order', string='Orden de Reparaciòn',
                                domain="[('state', 'in', ['draft','confirmed','under_repair','ready','2binvoiced','invoice_except'])]")
    