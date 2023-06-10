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
    motif_rejet = fields.Text(string='Motif de rejet', tracking=True)
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
    status = fields.Selection([('nonentamne','Non entamne'),
                            ('endefinition',"Definition de l'action"),
                            ('enattentevalidation','En attente de validation'),
                            ('encours','Encours'),
                            ('enattenteaproba',"En attente d'approbation"),
                            ('approuve','Approuve'),
                            ('realise','Realise'),
                            ('solde','Solde'),
                            ('abandonner','Abandonner')
                            ],default='nonentamne',string="Statut",tracking=True)
    pilote_id = fields.Many2one('plan.employe', string='Pilote',tracking=True)
    constat_id = fields.Many2one('plan.constat', string='Constat')
    direction_id = fields.Many2one('plan.direction', string='Direction')


    def send_mail_notification(self, template):
        template_id = self.env.ref(template)
        for rec in self:
            template_id.send_mail(rec.id, force_send=True)
            
            return True
        return False

    def redefinir_action(self):
        
        # self.send_mail_notification(template)
        #notify pilote 
        return {
            'name': 'Redefinir Action',
            'type': 'ir.actions.act_window',
            'res_model': 'plan.rejet.action',
            'view_mode': 'form',
            'view_id': self.env.ref('plan.plan_rejet_action_form_view').id,
            'target': 'current',
            'context': {
                'default_action_id': self.id,
            }


        }
    
    def valider_action(self):
        #notify pilote
        print('***********EXECUTING VALIDER************')
        print('++++++++++++++++++++++',self)
        
        self.motif_rejet = False
        template = 'plan.valider_action_mail'
        print(template)
        self.send_mail_notification(template)
        self.status = 'encours'
        return 
    
    def approuver_action(self):
        if self.type_action == 'corrective':
            self.status = 'realise'
            self.constat_id.status = 'traite'
            template = 'plan.action_corrective_traite_mail'
            self.send_mail_notification(template)
            return
        
            #notify direction pilote: directeur, refrerent, pilote
        template = 'plan.action_approuver_mail'
        self.send_mail_notification(template)
        self.status = 'solde'
        #notify direction pilote: directeur, refrerent, pilote
        #check if all actions are solde
        all_actions_solded = self.constat_id.check_if_all_actions_solded()
        if all_actions_solded:
            print('***********ALL ACTIONS SOLDED************')
            self.constat_id.status = 'solde'
            print(self.constat_id.status)
            return True
        return False
    
    def desapprouver_action(self):
        self.taux_avancement = self.taux_avancement - 10
        template = 'plan.action_desapprouver_mail'
        self.send_mail_notification(template)
        return
    
    def abandonner_action(self):
        self.status = 'abandonner'
        template = 'plan.action_abandonner_mail'
        self.send_mail_notification(template)
        return

    def write(self, values):
        if 'status' not in values:
            values['status'] = 'enattentevalidation'
        record = super().write(values)
        if record:
            template = 'plan.action_definie_mail'
            self.send_mail_notification(template)
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
        return {
        'name': 'Renseigner Taux Avancement',
        'type': 'ir.actions.act_window',
        'res_model': 'plan.taux.avancement.action',
        'view_mode': 'form',
        'view_id': self.env.ref('plan.plan_taux_avancement_action_form_view').id,
        'target': 'current',
        'context': {
            'default_action_id': self.id,
        }
        }
    
    def mesure_efficacite(self):
        return {
            'name': 'Mesure Efficacite',
            'type': 'ir.actions.act_window',
            'res_model': 'plan.mesure.efficacite',
            'view_mode': 'form',
            'view_id': self.env.ref('plan.plan_mesure_efficacite_form_view').id,
            'target': 'current',
            'context': {
                'default_action_id': self.id,
                }
            }
    
    
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.action))
        return res
    
    def get_createur_constat(self):
        directeur_email = self.sudo().constat_id.create_uid.email
        return str(directeur_email)