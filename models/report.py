
from odoo import api, models, fields, tools

class ReporteRMA(models.Model):
    _name = 'method_repair_cost.report_general_rma'
    _description = "Reporte general de RMA"
    _auto = False
    # _order = 'fecha_dia'

    fecha = fields.Date(string='Fecha')
    rma = fields.Char(string='RMA')
    sku = fields.Char(string='SKU')
    product_id = fields.Many2one(comodel_name='product.product', string='Producto')
    product_tmpl_id = fields.Many2one(comodel_name='product.teplate', string='PlantillaProducto')
    estado = fields.Char(string='Estado')
    metodofacturacion = fields.Char(string='Metodo Facturacion')
    neto = fields.Integer(string='Neto')
    impuesto = fields.Integer(string='Impuesto')
    total = fields.Integer(string='total')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')
    equipo_id = fields.Many2one(comodel_name='emsin.equipos', string='Equipos')    
    total_costo = fields.Integer(string='Costo Total')
    margen = fields.Integer(string='margen')
    costeo_inventario = fields.Integer(string='Costo Inventario')
    costeo_facturas = fields.Integer(string='Costo Facturas Compra')
    costeo_hh = fields.Integer(string='Costeo HH')
    costeo_hh_normal = fields.Integer(string='Costeo HH Normal')
    costeo_hh_50 = fields.Integer(string='Costeo HH 50%')
    costeo_hh_100 = fields.Integer(string='Costeo HH 100%')
    costeo_otros = fields.Integer(string='Total Otros Costos')
    costeo_inventario_porc = fields.Float(string='% Costo Inventario')
    costeo_facturas_porc = fields.Float(string='% Costo Facturas')
    costeo_hh_porc = fields.Float(string='% Costo HH')
    costeo_hh_normal_porc = fields.Float(string='% Costo HH Normal')
    costeo_hh_50_porc = fields.Float(string='% Costo HH 50%')
    costeo_hh_100_porc = fields.Float(string='% Costo HH 100%')
    costeo_otros_porc = fields.Float(string='% Otros Costos')
    total_costo_porc = fields.Float(string='% Total Costos')
    margen_porc = fields.Float(string='% Margen')

    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (SELECT 
                    ROW_NUMBER() OVER() AS id,
                    ro.create_date fecha,ro.name rma,pp.default_code sku,ro.product_id ,pp.product_tmpl_id ,ro.state estado,
                    ro.invoice_method metodofacturacion,ro.amount_untaxed neto,ro.amount_tax impuesto,ro.amount_total total,
                    ro.partner_id, ro.equipo_id,ro.total_costo,ro.margen,ro.costeo_inventario ,ro.costeo_facturas,ro.costeo_hh,
                    ro.costeo_hh_normal,ro.costeo_hh_50,ro.costeo_hh_100,ro.costeo_otros,ro.costeo_inventario_porc,
                    ro.costeo_facturas_porc,ro.costeo_hh_porc,ro.costeo_hh_normal_porc,ro.costeo_hh_50_porc,ro.costeo_hh_100_porc,
                    ro.costeo_otros_porc,ro.total_costo_porc,ro.margen_porc  
                    from repair_order ro,res_partner rp,product_product pp,product_template pt  
                    where ro.partner_id =rp.id 
                    and ro.product_id =pp.id 
                    and pp.product_tmpl_id =pt.id 
  
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))



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
    tipo =fields.Selection([('normal','Normal X Factor'),
                            ('50','HH Extra 50%'),
                            ('100','HH Extra 100%')],string='Tipo')

    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (SELECT 
                    ROW_NUMBER() OVER() AS id,
                    mrcch.employee_id,mrcch.cantidad_hh, mrcch.repair_id,mrcch.fecha_hh,mrcch.costo_hora,mrcch.costo_total_hora,
                    mrcch.tipo
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