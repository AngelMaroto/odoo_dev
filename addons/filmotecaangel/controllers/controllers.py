# -*- coding: utf-8 -*-
# from odoo import http


# class Filmotecaangel(http.Controller):
#     @http.route('/filmotecaangel/filmotecaangel', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/filmotecaangel/filmotecaangel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('filmotecaangel.listing', {
#             'root': '/filmotecaangel/filmotecaangel',
#             'objects': http.request.env['filmotecaangel.filmotecaangel'].search([]),
#         })

#     @http.route('/filmotecaangel/filmotecaangel/objects/<model("filmotecaangel.filmotecaangel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('filmotecaangel.object', {
#             'object': obj
#         })

