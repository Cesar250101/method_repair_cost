# -*- coding: utf-8 -*-
from odoo import http

# class MethodRepairCost(http.Controller):
#     @http.route('/method_repair_cost/method_repair_cost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/method_repair_cost/method_repair_cost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('method_repair_cost.listing', {
#             'root': '/method_repair_cost/method_repair_cost',
#             'objects': http.request.env['method_repair_cost.method_repair_cost'].search([]),
#         })

#     @http.route('/method_repair_cost/method_repair_cost/objects/<model("method_repair_cost.method_repair_cost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('method_repair_cost.object', {
#             'object': obj
#         })