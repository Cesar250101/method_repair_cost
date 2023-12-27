# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Rma(models.Model):
    _inherit = 'hr.employee'

    costeo_rma = fields.Boolean(string='Excluir del costeo RMA?')

    