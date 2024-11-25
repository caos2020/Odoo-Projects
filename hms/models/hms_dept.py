from odoo import models, fields
class Department(models.Model):
    _name = 'hospital.department'
    name=fields.Char()
    capacity=fields.Integer()
    is_opened=fields.Boolean()
    patients_ids=fields.One2many('hospital.patient','dept_id')
