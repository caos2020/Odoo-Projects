# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json

class CRMRegistrationController(http.Controller):

    @http.route('/api/crm/register', type='json', auth='public', methods=['POST'], csrf=False)
    def register_crm_lead(self, **kwargs):

        args = request.httprequest.data.decode()
        vals = json.loads(args)


        try:
            res = request.env['crm.lead'].sudo().create(vals)

            return {
                "success": True,
                "message": "success",
                "lead_id": res.id
            }

        except Exception as e:
            return {"error": str(e)}
