# -*- coding: utf-8 -*-
# from odoo import http


# class Plan(http.Controller):
#     @http.route('/plan/plan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/plan/plan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('plan.listing', {
#             'root': '/plan/plan',
#             'objects': http.request.env['plan.plan'].search([]),
#         })

#     @http.route('/plan/plan/objects/<model("plan.plan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('plan.object', {
#             'object': obj
#         })
