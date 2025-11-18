#-*- coding: utf-8 -*-

from odoo import models, fields, api


class tecnica(models.Model):
    _name = 'filmotecaangel.tecnica'
    _description = 'filmotecaangel.tecnica'

    name = fields.Char(string="Nombre")
    description = fields.Text(string="Descripción")
    photo=fields.Binary(string="Imagen")

    peliculas_id = fields.Many2many(comodel_name = "filmotecaangel.pelicula",
                                    relation = "tecnicas_peliculas",
                                    column1 = "tecnica_id",
                                    column2 = "pelicula_id",
                                    string = "Películas")
