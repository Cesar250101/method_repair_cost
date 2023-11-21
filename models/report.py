
from odoo import api, models, fields, tools

class Ventas(models.Model):
    _name = 'method_repair_cost.rma_hh_report'
    _description = "Reporte de horas por RMA"
    _auto = False
    # _order = 'fecha_dia'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Empleado')
    cantidad_hh = fields.Float(string='N° Hotras')
    repair_id = fields.Many2one(comodel_name='repair.order', string='RMA')
    fecha_hh = fields.Date(string='Fecha')
    costo_hora = fields.Integer(string='Costo Hora')
    costo_total_hora = fields.Integer(string='Total Horas')

    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (SELECT 
                    ROW_NUMBER() OVER() AS id,
                    mrcch.employee_id,mrcch.cantidad_hh, mrcch.repair_id,mrcch.fecha_hh,mrcch.costo_hora,mrcch.costo_total_hora  
                    from method_repair_cost_costo_hh mrcch,hr_employee he,repair_order ro 
                    where mrcch.employee_id =he.id 
                    and mrcch.repair_id =ro.id  
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))

class Ventas(models.Model):
    _name = 'method_repair_cost.salidas_stock_report'
    _description = "Reporte de salidas de inventario por RMA"
    _auto = False
    # _order = 'fecha_dia'

    date_done = fields.Datetime(string='Fecha Salida')
    repair_id = fields.Many2one(comodel_name='repair.order', string='RMA')
    categ_id = fields.Many2one(comodel_name='product.category', string='Categoria')
    product_id = fields.Many2one(comodel_name='product.product', string='Productos')
    product_qty = fields.Integer(string='Cantidad')
    costo = fields.Integer(string='Costo')
    costo_total = fields.Integer(string='Costo Total')
    name = fields.Char(string='Picking')

    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (SELECT 
                    ROW_NUMBER() OVER() AS id,
                    sp.date_done,sp.repair_id,pt.categ_id,sm.product_id,sm.product_qty,
                    coalesce((select cost from product_price_history pph where pph.product_id=pp.id order by create_date desc limit 1),0) Costo,
                    coalesce((select cost from product_price_history pph where pph.product_id=pp.id order by create_date desc limit 1),0)*sm.product_qty costo_total,
                    sp.name
                    from stock_picking sp,stock_move sm,product_product pp,product_template pt,product_category pc  
                    where coalesce(sp.repair_id,0)!=0 
                    and sp.state ='done'
                    and sp.id=sm.picking_id 
                    and sm.product_id =pp.id 
                    and pp.product_tmpl_id =pt.id 
                    and pt.categ_id =pc.id  
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))        