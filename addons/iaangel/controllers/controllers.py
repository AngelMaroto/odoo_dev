# -*- coding: utf-8 -*-
# from odoo import http


# class Iaangel(http.Controller):
#     @http.route('/iaangel/iaangel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iaangel/iaangel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iaangel.listing', {
#             'root': '/iaangel/iaangel',
#             'objects': http.request.env['iaangel.iaangel'].search([]),
#         })

#     @http.route('/iaangel/iaangel/objects/<model("iaangel.iaangel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iaangel.object', {
#             'object': obj
#         })

