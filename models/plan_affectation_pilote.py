from odoo import fields, models, api

class AffectationPilote(models.Model):
    _name = 'plan.affectation_pilote'
    _description = 'Affectation Pilote'


    # _inherit = ['mail.thread', 'mail.activity.mixin']

    origine_constat = fields.Char(string='Origine Constat')
    type_constat = fields.Char(string='Type Constat')
    direction_pilote_id = fields.Many2one('plan.direction', string='Direction pilote')
    pilote_id = fields.Many2one('plan.employe', string='Pilote',domain="[('direction_id','=',direction_pilote_id)]")
    constat_id = fields.Many2one('plan.constat', string='Constat')
    action_id = fields.Many2one('plan.action', string='Action')

    # def ajouter_action(self):
    #     return 
    
    def send_mail_notification(self):
        template_id = self.env.ref('plan.affectation_pilote_mail')
        for rec in self:
            print('**********SEND MAIL INVOKED*********')
            template_id.send_mail(rec.id, force_send=True)

    def get_affectation_pilote_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # http://localhost:8069/web#id=3&action=136&model=plan.affectation_pilote&view_type=form&cids=&menu_id=114
        # http://localhost:8069/web#id=1
        affectation_url = base_url + '/web#id=' + str(self.id) + '&action=127&model=plan.affectation_pilote&view_type=form&cids=&menu_id=105'
        print(affectation_url)
        return affectation_url
    
    def write(self, vals):
        print('**********WRITE INVOKED*********')
        if not vals['pilote_id']:
            return
        record = super(AffectationPilote, self).write(vals)
        # domain = ['&',('direction_id','=',self.direction_pilote_id.id),('constat_id','=',self.constat_id.id)]
        # action_concerne = self.env['plan.action'].search(domain)
        print(self.action_id)
        print(self.pilote_id)
        self.action_id.pilote_id = self.pilote_id
        template = 'plan.pilote_affecte_email'
        # print(action_concerne)
        action_concerne = self.action_id
        print(action_concerne)
        action_concerne.status = 'endefinition'
        action_concerne.send_mail_notification(template)
        return record
        # notify pilote

    @api.model
    def create(self, vals):
        record = super(AffectationPilote, self).create(vals)
        record.send_mail_notification()
        return record   

