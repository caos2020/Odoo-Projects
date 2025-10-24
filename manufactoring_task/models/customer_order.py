from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        readonly=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='sale_id.partner_id',
        store=True,
        readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.origin:
                sale_order = self.env['sale.order'].search([('name', '=', record.origin)], limit=1)
                if sale_order:
                    record.sale_id = sale_order.id
        return records

    # product_list_text = fields.Char(
    #     string="Products",
    #     compute="_compute_product_list_text",
    #     store=False
    # )
    #
    # @api.depends('move_finished_ids.product_id')
    # def _compute_product_list_text(self):
    #     for record in self:
    #         product_names = record.move_finished_ids.mapped('product_id.name')
    #         record.product_list_text = ' + '.join(product_names) if product_names else record.product_id.display_name