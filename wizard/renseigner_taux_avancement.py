from odoo import fields, models, api

class ResnseignementTauxAvancement(models.TransientModel):
    _name = 'plan.renseigner.taux.avancement.wizard'
    _description = 'Renseigner Taux Avancement'

    action_id = fields.Many2one('plan.action', string='Action')
    motif_rejet = fields.Text(string='Motif de rejet')
