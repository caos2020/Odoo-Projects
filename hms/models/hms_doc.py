from odoo import fields, models


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _rec_name = 'first_name'
    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()







