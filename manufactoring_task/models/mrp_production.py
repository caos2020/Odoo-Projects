from odoo import models
import io
import base64
import xlsxwriter
from datetime import datetime

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_export_excel(self):
        import io, base64, xlsxwriter
        from datetime import datetime

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("MO Components")

        bold = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        normal = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
        total_fmt = workbook.add_format({'bold': True, 'bg_color': '#D9EAD3', 'border': 1, 'align': 'center'})

        headers = ['MO Reference', 'Customer', 'Start Date', 'Component Code', 'Component Name', 'Quantity']
        for col, h in enumerate(headers):
            sheet.write(0, col, h, bold)

        row = 1
        totals = {}

        for mo in self:
            mo_ref = mo.name or ''
            customer = mo.customer_id.name if mo.customer_id else ''
            date_val = mo.date_start.strftime('%Y-%m-%d') if mo.date_start else ''

            for move in mo.move_raw_ids:
                product = move.product_id
                if not product:
                    continue
                qty = move.product_uom_qty or 0.0

                sheet.write(row, 0, mo_ref, normal)
                sheet.write(row, 1, customer, normal)
                sheet.write(row, 2, date_val, normal)
                sheet.write(row, 3, product.default_code or '', normal)
                sheet.write(row, 4, product.display_name or '', normal)
                sheet.write(row, 5, qty, normal)

                totals[product.id] = totals.get(product.id, 0.0) + qty
                row += 1


        row += 2
        sheet.write(row, 3, 'Total Quantity per Component', total_fmt)
        sheet.write(row, 4, '', total_fmt)
        sheet.write(row, 5, '', total_fmt)
        row += 1

        for product_id, qty in totals.items():
            product = self.env['product.product'].browse(product_id)
            sheet.write(row, 3, product.default_code or '', normal)
            sheet.write(row, 4, product.display_name or '', normal)
            sheet.write(row, 5, qty, normal)
            row += 1


        sheet.set_column('A:A', 18)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 12)

        workbook.close()
        output.seek(0)
        data = base64.b64encode(output.read())
        output.close()

        attachment = self.env['ir.attachment'].create({
            'name': f'MO_Components_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            'type': 'binary',
            'datas': data,
            'res_model': 'mrp.production',
            'public': False,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
