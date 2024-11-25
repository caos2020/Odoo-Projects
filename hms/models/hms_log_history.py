from odoo import models, fields

class LogHistory(models.Model):
    _name = 'hospital.loghistory'
    _rec_name = 'desc'
    desc=fields.Text()
    patient_id=fields.Many2one('hospital.patient')

    # write_date
