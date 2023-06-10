from odoo import fields,models,api

class PlanMesureEfficacite(models.Model):
    _name = 'plan.mesure.efficacite'
    _description = 'Plan de mesure d\'efficacité'

    action_id = fields.Many2one('plan.action', string='Action')
    mesure_efficacite = fields.Selection([('concluante','Concluante'),
                                    ('non_concluante','Non Concluante')],string="Efficacité",required=True)
