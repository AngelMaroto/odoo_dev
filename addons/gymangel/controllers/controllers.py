# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class GymController(http.Controller):

    # 1. Endpoint para obtener la lista de clases (GET)
    # Se accede por: http://localhost:8069/api/gym/sessions
    @http.route('/api/gym/sessions', auth='public', methods=['GET'], csrf=False)
    def get_sessions(self, **kw):
        # Buscamos todas las sesiones en la base de datos
        sessions = request.env['gym.session'].sudo().search([])
        
        # Preparamos una lista de diccionarios (JSON compatible)
        data = []
        for s in sessions:
            data.append({
                'id': s.id,
                'nombre': s.name,
                'actividad': s.activity_id.name,
                'fecha': str(s.start_date),
                'plazas_libres': s.available_seats,
                'porcentaje_ocupacion': s.occupied_percentage,
            })
            
        # Devolvemos la respuesta en formato JSON
        return request.make_response(
            json.dumps(data),
            headers=[('Content-Type', 'application/json')]
        )