# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Response
import json

class Filmotecaangel(http.Controller):
    @http.route('/api/peliculas', auth='public', method=['GET'], csrf=False)
    def get_peliculas(self, **kw):
        try:
            peliculas = http.request.env['filmotecaangel.pelicula'].sudo().search_read([],['id','name','color'])
            res =json.dumps(peliculas, ensure_ascii=False).encode('utf-8')
            return Response(res, content_type='application/json;charset=utf-8', status=200)
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json;charset=utf-8', status=200)

    # @http.route('/filmotecaangel/filmotecaangel', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"

    # @http.route('/filmotecaangel/filmotecaangel/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('filmotecaangel.listing', {
    #         'root': '/filmotecaangel/filmotecaangel',
    #         'objects': http.request.env['filmotecaangel.filmotecaangel'].search([]),
    #     })

    # @http.route('/filmotecaangel/filmotecaangel/objects/<model("filmotecaangel.filmotecaangel"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('filmotecaangel.object', {
    #         'object': obj
    #     })

