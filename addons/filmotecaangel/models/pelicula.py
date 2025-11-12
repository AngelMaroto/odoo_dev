#-*- coding: utf-8 -*-

from odoo import models, fields, api


class pelicula(models.Model):
    _name = 'filmotecaangel.pelicula'
    _description = 'filmotecaangel.pelicula'

    name = fields.Char(string="Nombre", readonly = False, required=True, help="Introduzca el nombre cariñin")
    description = fields.Text()
    film_date = fields.Date()
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    is_spanish = fields.Boolean()

    genero_id = fields.Many2one("filmotecaangel.genero", string="Género", required=True, ondelete="cascade")
    tecnicas_id = fields.Many2many("filmotecaangel.tecnica")
    
    image = fields.Binary(string="Imagen", help="suba la imagen")
    language = fields.Selection([('es','Español'),
                                ('en','Inglés'),
                                ('fr','Francés'),
                                ('de','Aleman'),
                                ('it','Italiano')],
                                string="Lenguaje",
                                required=True,
                                default='es',
                                help='Seleccione el lenguaje de la pelicula')
    
    opinion = fields.Selection([('0','mala'),
                               ('1','regular'),
                               ('2','buena')],
                               string="Opinion",
                               required=True,
                               default='1')
    
    color = fields.Selection([('bn','Blanco y negro'),
                             ('cl','Color')],
                             string='Color',
                             required=True)