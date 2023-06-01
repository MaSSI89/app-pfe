from odoo import fields, models

class Processus(models.Model):
    _name = 'plan.processus'
    _description = 'Processus'

    name = fields.Char(string='Nom Processus', required=True)
    directeur_id = fields.Many2one('plan.employe', string='Directeur', required=True)
    unite_id = fields.Many2one('plan.unite', string='Unité', required=True)