from odoo import fields, models, api

class RejetAction(models.Model):
    _name = 'plan.rejet.action'
    _description = 'Rejet Action'

    action_id = fields.Many2one('plan.action', string='Action')
    motif_rejet = fields.Char(string='Motif Rejet :')

    @api.model
    def create(self,vals):
        record = super(RejetAction, self).create(vals)
        record.action_id.motif_rejet = record.motif_rejet
        record.action_id.status = 'endefinition'
        template = 'plan.redefinir_action_mail'
        record.action_id.send_mail_notification(template)
        return record