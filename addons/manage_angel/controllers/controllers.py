# -*- coding: utf-8 -*-
# from odoo import http


# class ManageAngel(http.Controller):
#     @http.route('/manage_angel/manage_angel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manage_angel/manage_angel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('manage_angel.listing', {
#             'root': '/manage_angel/manage_angel',
#             'objects': http.request.env['manage_angel.manage_angel'].search([]),
#         })

#     @http.route('/manage_angel/manage_angel/objects/<model("manage_angel.manage_angel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manage_angel.object', {
#             'object': obj
#         })

