# -*- coding: utf-8 -*-
{
    'name': "method_repair_cost",

    'summary': """
                Ayudar a determinar el costo de una orden de reparaciòn
        """,

    'description': """
        El costo se determina con los siguientes conceptos:
        -Salidas de inventario
        -Horas trabajadas por empleados en la RMA
        -Facturas de compras por servicios de terceros
    """,

    'author': "Method ERP",
    'website': "https://www.method.cl",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','repair'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking.xml',
        'views/templates.xml',
        'views/account_invoice.xml',
        'views/repair_order.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}