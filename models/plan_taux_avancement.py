from odoo import fields , models, api, _
from odoo.exceptions import ValidationError

class TauxAvancementAction(models.Model):
    _name = 'plan.taux.avancement.action'
    _description = 'Taux Avancement Action'

    taux_avancement = fields.Integer(string='Taux d\'avancement', default=0,tracking=True)
    action_id = fields.Many2one('plan.action', string='Action')

    @api.model
    def create(self, vals):
        if vals['taux_avancement'] > 100:
            raise ValidationError(_('Le taux d\'avancement ne peut pas dépasser 100'))
        
        record = super(TauxAvancementAction, self).create(vals)
        record.action_id.taux_avancement = record.taux_avancement
        if record.taux_avancement == 100:
            
            template = 'plan.demande_approbation_action_mail'
            record.action_id.status = 'enattenteaproba'
            record.action_id.send_mail_notification(template)
            return record
        
        return record

