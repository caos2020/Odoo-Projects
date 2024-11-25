from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError



class HmsPatient(models.Model):
    _name = 'hospital.patient'
    _rec_name = 'first_name'
    first_name = fields.Char(string='Patient First Name')
    last_name = fields.Char(string='Patient Last Name')
    birth_date = fields.Date()
    email = fields.Char()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A', 'A'), ('A+', 'A+'), ('B', 'B'), ('B-', 'B-'), ('AB', 'AB')], default='A')
    bcr = fields.Boolean('BCR')
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute='_getAge',store=True)
    dept_id = fields.Many2one('hospital.department')
    is_opened = fields.Boolean(related='dept_id.is_opened')
    dept_capacity = fields.Integer(related='dept_id.capacity')
    state = fields.Selection(
        [('Undetermined', 'Undetermined'), ('Good', 'Good'), ('Fair', 'Fair'), ('Serious', 'Serious')])
    doc_ids = fields.Many2many('hospital.doctor')
    doc_name = fields.Char(related='doc_ids.first_name')
    log_ids = fields.One2many('hospital.loghistory', 'patient_id')

    @api.depends('birth_date')
    def _getAge(self):
        for patient in self:
            if patient.birth_date:
                today=fields.Date.today()
                delta= (today - patient.birth_date).days
                patient.age=delta // 365
            else:
                patient.age = 0

    @api.onchange('age')
    def change_bcr(self):
        if self.age < 30:
            self.bcr = True
            return {
                'warning':
                    {
                        'title': 'Bcr Changing',
                        'message': 'Bcr Value has been changed To True because age<30'
                     }
             }


    @api.model
    def create(self, vals):
        email=vals['email']
        if not '@' in email:
            raise UserError("Email is    not Valid")
        return super().create(vals)
    #
    def write(self, vals):
        email=vals['email']
        if not '@' in email:
            raise UserError("Email is not Valid")

        super().write(vals)
    def action_state_Undetermined(self):
        self.state = 'Undetermined'
        self.env['hospital.loghistory'].create({'desc':f"state is{self.state}"})


    def action_state_Good(self):
        self.state = 'Good'
        self.env['hospital.loghistory'].create({'desc':f"state is{self.state}"})


    def action_state_Fair(self):
        self.state = 'Fair'
        self.env['hospital.loghistory'].create({'desc':f"state is{self.state}"})



    def action_state_Serious(self):
        self.state = 'Serious'
        self.env['hospital.loghistory'].create({'desc':f"state is{self.state}"})
    _sql_constraints = [('Unique_Email','unique (email)','This Email is already exists')]


