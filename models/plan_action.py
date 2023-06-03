from odoo import fields, models,api,_
from odoo.exceptions import ValidationError

class Action(models.Model):
    _name = 'plan.action'
    _description = 'Action'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    action = fields.Text(string='Action',tracking=True)
    date_creation = fields.Date(string='Date de création', default=fields.Date.today, tracking=True)
    date_fin_previsionelle = fields.Date(string='Date de fin prévisionelle', tracking=True)
    risque = fields.Text(string='Risque',tracking=True)
    cause = fields.Text(string='Cause')
    opportunite = fields.Text(string='Opportunité')
    taux_avancement = fields.Integer(string='Taux d\'avancement', default=0,tracking=True)
    motif_rejet = fields.Text(string='Motif de rejet')
    statut_approbation = fields.Selection([('pasEncore', 'Pas Encore'),
                                            ('approuve', 'Approuve'),
                                            ('Disapprouve', 'Disapprouve')
                                            ],default="pasEncore",tracking=True)
    type_risque = fields.Selection([('qualite','Qualite'),
                                    ('finance', 'Finance')],tracking=True)
    type_action = fields.Selection([
                                    ('corrective','Action Corrective'),
                                    ('preventive','Action Preventive'),
                                    ('amelioration','Action Amelioration'),
                                    ('non_retenue', 'Non Retenue')
                                    ],string="Type Action")
    status = fields.Selection([
                            ('solde','Solde'),
                            ('abandonner','Abandonnée'),
                            ('realise','Realise'),
                            ('approuve','Approuvée'),
                            ('enattenteaproba',"En attente d'approbation"),
                            ('encours','Encours'),
                            ('enattentevalidation','En attente de validation'),
                            ('endefinition',"Definition de l'action"),
                            ('nonentamne','Non entamne'),
                            ],default='nonentamne',string="Statut",tracking=True)
    pilote_id = fields.Many2one('plan.employe', string='Pilote')
    constat_id = fields.Many2one('plan.constat', string='Constat')
    direction_id = fields.Many2one('plan.direction', string='Direction')


    def send_mail_notification(self, template):
        template_id = self.env.ref(template)
        for rec in self:
            template_id.send_mail(rec.id, force_send=True)
            
            return True
        return False

    def redefinir_action(self):
        template = 'plan.redefinir_action_mail'
        self.send_mail_notification(template)
        #notify pilote 
        return
    
    def valider_action(self):
        #notify pilote
        self.status = 'encours'
        template = 'plan.valider_action_mail'
        self.send_mail_notification(template)
        return
    
    def approuver_action(self):
        if self.type_action == 'corrective':
            self.status = 'realise'
            #notify direction pilote: directeur, refrerent, pilote
        else:
            self.status = 'solde'
            #notify direction pilote: directeur, refrerent, pilote
            #check if all actions are solde
            all_actions_solded = True
            if all_actions_solded:
                self.constat_id.status = 'solde'
                #notify direction pilote: Administrateur, createur constat, referent , pilote

        return
    
    def desapprouver_action(self):
        return
    
    def abandonner_action(self):
        self.status = 'abandonner'
        return

    def write(self, values):
        if 'status' not in values:
            values['status'] = 'enattentevalidation'
        record = super().write(values)
        return record
        
    def get_action_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # http://localhost:8069/web#id=8&action=135&model=plan.action&view_type=form&cids=1&menu_id=114
        action_url = base_url + '/web#id=' + str(self.id) + '&action=135&model=plan.action&view_type=form&cids=1&menu_id=114'
        return action_url
    
    def verify_action_date_fin_previsionelle(self):
        today = fields.Date.today()
        domain = ['&',('date_fin_previsionelle', '=', today),('taux_avancement','<', 100)]
        actions = self.env['plan.action'].search(domain)
        template = 'plan.action_date_fin_previsionelle_email'
        print(actions)
        for action in actions:

            action.send_mail_notification(template)

    def renseigner_taux_avancement(self):
        return True