#-*- coding: utf-8 -*-

from odoo import models, fields, api


class genero(models.Model):
    _name = 'filmotecaangel.genero'
    _description = 'filmotecaangel.genero'

    name = fields.Char(string="Nombre", readonly = False, required=True, help="Introduzca el nombre")
    description = fields.Text()
    intriga = fields.Boolean()
    infantil = fields.Boolean()

    peliculas_id = fields.One2many(string="Películas", comodel_name="filmotecaangel.pelicula", inverse_name="genero_id")