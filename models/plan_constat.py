from odoo import fields, models,api,_

class Constat(models.Model):
    _name = 'plan.constat'
    _description = 'Constat'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    document = fields.Binary(string='Document')
    name = fields.Text(string='Nom', required=True)
    genere_action = fields.Boolean(string='Générer action', required=True)
    type_constat = fields.Selection([('fort','Point fort'),
                                     ('progre','Piste de Progres'),
                                     ('sensible','Point Sensible'),
                                     ('recommendation','Recommendation'),
                                     ('recommendation_maj','Recommendation Majeure'),
                                     ('observation','Observation')],string="Type Constat")
    status = fields.Selection([('ouvert','Ouvert'),
                               ('encours','En cours'),
                               ('traite','Traite'),
                               ('solde','Solde'),
                               ('annule','Annule')
                               ,('supprime','Supprime')],default="ouvert")
    origine = fields.Selection([
                            ('blanc', 'Audit à blanc'),
                            ('ema', 'Audit externe EMA'),
                            ('iso45', 'Audit externe ISO 45001'),
                            ('iso90', 'Audit externe ISO 9001'),
                            ('2iso', 'Audit externe iso 9001 et 45001'),
                            ('externe', 'Audit externe métier'),
                            ('interne', 'Audit interne'),
                            ('bhe', 'BHE'),
                            ('boite', 'Boite à idée'),
                            ('mystere', 'Enquête mystère QdS'),
                            ('satisfactionVOyage', 'Enquête satisfaction voyageurs'),
                            ('satisfactionEMA', 'Enquêtes satisfaction EMA'),
                            ('exercices', 'Exercices / Simulations'),
                            ('fiche', 'Fiche d\'Amélioration et de Progrès'),
                            ('incident', 'incident / Accident'),
                            ('innov', 'Innov & Go'),
                            ('hse', 'Inspection HSE'),
                            ('qualite', 'Inspection Qualité'),
                            ('securite', 'Inspection sécurité ferroviaire'),
                            ('inspectionSecurite', 'Inspection sécurité incendie'),
                            ('inspectionSurete', 'Inspection Sureté'),
                            ('rapportAnnuel', 'Rapport Annuel d\'Activité'),
                            ('rapportMensuel', 'Rapport Mensuel d\'Activité'),
                            ('rapportMetier', 'Rapport Métier'),
                            ('revueDirection', 'Revue de Direction'),
                            ('revueAmelioration', 'Revue du Plan d\'Amélioration'),
                            ('riskManagement', 'Risk management'),
                            ('conformite', 'Conformité légale'),
                            ('auditCertification', 'Audit de certification')],'Origine')
    direction_concerne_ids = fields.Many2one('plan.direction',string='Direction concernée',)
    direction_pilote_ids = fields.Many2many('plan.direction',string='Direction pilote')
    activite_id = fields.Many2one('plan.unite', string='Unite')
    processus_id = fields.Many2one('plan.processus', string='Processus')
    action_ids = fields.One2many('plan.action','constat_id', string='Action')
    affectation_pilote_ids = fields.One2many('plan.affectation_pilote', 'constat_id', string='Affectation')


    def supprimer_constat(self):
        self.status = 'supprime'
        # notify constat createur
        return
    
    def annuler_constat(self):
        self.status = 'annule'
        # notify constat createur
        return

    @api.model
    def create(self, vals):
        record = super(Constat, self).create(vals)
        if not vals['genere_action'] and vals['type_constat'] == 'fort':
            #notify direction pilote directeur et referent
            a=1
        
        for rec in vals['direction_pilote_ids'][0][2]:
            action = {
                'direction_id': rec,
                'constat_id': record.id,
            }
            action_record = self.env['plan.action'].create(action)
            affectation_pilote = {
                'constat_id': record.id,
                'direction_pilote_id': rec,
                'origine_constat': record.origine,
                'type_constat': record.type_constat,
                'action_id': action_record.id,
            }
            affectation_pilote_record = self.env['plan.affectation_pilote'].create(affectation_pilote)
            # affectation_pilote_record.send_mail_notification()
        # notify direction pilote directeur referent providing affectation pilote link
        return record





    @api.onchange('direction_pilote_ids')
    def onchange_direction_pilote(self):
        if self.direction_pilote_ids:
            print('*******************')
            print(self.direction_pilote_ids)
            unites_ids = self.direction_pilote_ids.ids
            print(unites_ids)
            unite_domain = [('direction_id','=', unites_ids[-1])]
            print(unite_domain)
            print('*******************')
            return {'domain': {'activite_id': unite_domain}}
        else:
            self.activite_id = False

    @api.onchange('activite_id')
    def onchange_unite(self):
        if self.activite_id:
            print('+++++++++++++++++++')
            processus_ids = self.activite_id
            print(processus_ids)
            processus_domain = [('unite_id','=', processus_ids[-1].id)]
            print(processus_domain)
            print('+++++++++++++++++++')

            return {'domain': {'processus_id': processus_domain}}
        else:
            self.processus_id = False