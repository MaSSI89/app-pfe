from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    employe_id = fields.One2many('plan.employe','user_id',ondelete="cascade", string='Employé')