#-*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class pelicula(models.Model):
    _name = 'filmotecaangel.pelicula'
    _description = 'filmotecaangel.pelicula'

    code = fields.Char(string="Código", compute="_get_code")
    name = fields.Char(string="Nombre", readonly = False, required=True, help="Introduzca el nombre")
    description = fields.Text()
    film_date = fields.Date()
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    is_spanish = fields.Boolean()

    genero_id = fields.Many2one("filmotecaangel.genero", string="Género", required=True, ondelete="cascade")
    tecnicas_id = fields.Many2many(comodel_name = "filmotecaangel.tecnica",
                                   relation = "tecnicas_peliculas",
                                   column1 = "pelicula_id",
                                   column2 = "tecnica_id",
                                   string = "Técnicas")
    
    def _get_code(self):
        for pelicula in self:
            if len(pelicula.genero_id) == 0:
                pelicula.code = "FILM_"+str(pelicula.id)
            else:
                pelicula.code = str(pelicula.genero_id.name).upper()+"_"+str(pelicula.id)

    def toggle_color(self):
        self.is_spanish = not self.is_spanish

    def f_create(self):
        pelicula={
            "name": "Prueba ORM",
            "color": "cl",
            "genero_id": 1,
            "start_date": str(datetime.date(2022,8,8))
        }
        print(pelicula)
        self.env['filmotecaangel.pelicula'].create(pelicula)

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