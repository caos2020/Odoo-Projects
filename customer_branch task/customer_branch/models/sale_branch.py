from reportlab.lib.validators import inherit

from odoo import models, fields, api
class SaleBranch(models.Model):
    _inherit = 'sale.order'

    branch=fields.Many2one('res.partner',
        string="Customer Branch",
        domain="[('parent_id', '=', partner_id)]"
    )

    @api.onchange('partner_id')
    def _onchange_partner_id_clear_branch(self):
        if self.partner_id:
            self.branch = False