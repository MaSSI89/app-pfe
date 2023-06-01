from odoo import fields, models,api


class Employe(models.Model):
    _name = 'plan.employe'
    _description = 'Employé'
    _inherits = {'res.users': 'user_id'}

    user_id = fields.Many2one('res.users', ondelete='cascade',required=True)

    matricule_cnas = fields.Integer(string='Matricule CNAS', required=True)
    post_occupe = fields.Char(string='Poste occupé', required=True)
    direction_id = fields.Many2one('plan.direction', string='Direction', required=True)
    # action_ids = fields.One2many('plan.action', 'employe_id', string='Actions')

    @api.onchange('login')
    def _onchange_login(self):
        if self.login :
            self.email = self.login
        else :
            self.email = False