from odoo import models,fields
class PartnerXlsx(models.AbstractModel):
    _name = 'report.plan.constat_report_template_excel'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, constats):
        print('dassadsasdadsds===========')
        sheet = workbook.add_worksheet('Constats')
        bold = workbook.add_format({'bold': True})
        
        sheet.write(0,4,'Rapport sur les constats',bold)
        
        sheet.write(2, 2, 'Nom', bold)
        sheet.write(2, 3, 'Type', bold)
        sheet.write(2,4,'Direction concernée',bold)
        sheet.set_column(2,4,20)
        sheet.write(2,5,'Direction(s) pilote(s)',bold)
        sheet.set_column(2,5,20)
        sheet.write(2, 6, 'Unité', bold)
        sheet.set_column(2,6,15)
        sheet.write(2, 7, 'Processus', bold)
        sheet.set_column(2,7,15)
        sheet.write(2, 8, 'Statut', bold)
        
        ligne =3
        col=2

        for obj in constats:
           
            sheet.write(ligne,col,obj.name)
            sheet.write(ligne,col+1,obj.type_constat)

            direction = obj.direction_concerne_ids.name
            sheet.write(ligne,col+2,direction)
            
            direction_pilote= obj.direction_pilote_ids
            dir_ligne=ligne
            for dir in direction_pilote:
                sheet.write(ligne,col+3,dir.name)
                dir_ligne+=1

            sheet.write(ligne,col+4,obj.activite_id.name)
            sheet.write(ligne,col+5,obj.processus_id.name)
            sheet.write(ligne,col+6,obj.status)
            
            ligne=dir_ligne
            col=2
        date   = fields.Date.today()
        string  = 'Le '+str(date)
        sheet.write(ligne+1,8,string)