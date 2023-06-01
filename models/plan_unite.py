from odoo import fields, models

class Unite(models.Model):
    _name = 'plan.unite'
    _description = 'Unité'

    name = fields.Char(string='Nom Unité', required=True)
    directeur_id = fields.Many2one('plan.employe', string='Directeur')
    direction_id = fields.Many2one('plan.direction', string='Direction')
    processus_id = fields.Many2one('plan.processus', string='Processus')