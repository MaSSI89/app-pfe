from odoo import fields, models

class Direction(models.Model):
    _name = 'plan.direction'
    _description = 'Direction'

    name = fields.Char(string='Nom Direction', required=True)
    cree_le = fields.Date(string='Crée le', required=True)
    directeur_id = fields.Many2one('plan.employe', string='Directeur')
    referent_id = fields.Many2one('plan.employe', string='Référent')
    unites_ids = fields.One2many('plan.unite', 'direction_id', string='Unités')
    employes_ids = fields.One2many('plan.employe', 'direction_id', string='Employés')
     