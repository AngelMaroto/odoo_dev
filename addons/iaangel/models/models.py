# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


# class iaangel(models.Model):
#     _name = 'iaangel.iaangel'
#     _description = 'iaangel.iaangel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class proyecto(models.Model):
    _name = 'iaangel.proyecto'
    _description = 'iaangel.proyecto'

    titulo = fields.Char(compute="_compute_titulo")
    descripcion = fields.Char(required = True)
    prioridad = fields.Integer(default = 1)
    urgente = fields.Boolean(string="¿Es urgente?", compute="_compute_urgente" ,store=True)
    en_espera = fields.Boolean(string="¿Esta en espera?", default=True)
    finalizado = fields.Boolean()
    imagen = fields.Image()
    fecha_creacion = fields.Datetime()
    #Si tuviese bien echa la funcion para conseguir la fecha de hoy
    # fecha_creacion = fields.Datetime(compute="_compute_fecha")
    fecha_modificacion = fields.Datetime()
    #Si tuviese bien echa la funcion para conseguir la fecha de hoy
    #fecha_modificacion = fields.Datetime(compute="_compute_fechaMod")

    #Un proyecto es de solo un laboratorio
    laboratorio_id = fields.Many2one('iaangel.laboratorio')
    #Un proyecto es de solo un cientifico
    cientifico_id = fields.Many2one('iaangel.cientifico')
    #Un proyecto solo tiene una especialidad
    especialidad_id = fields.Many2one('iaangel.especialidad')
    #Un proyecto puede tener varios recursos
    recurso_id = fields.Many2many('iaangel.recurso')
    
#    def _compute_titulo(self):
#        prio = ""
#        for proyecto in self:
#            if proyecto.prioridad > 7 : {prio}="Urgente"
#            else : {prio}="Prioridad {proyecto.prioridad}"
#            proyecto.titulo = f"{laboratorio.nombre} - {prio} - Proyecto {proyecto.id}" if proyecto.id else "Proyecto nuevo"

    def _compute_titulo(self):
        for proyecto in self:
            proyecto.titulo = f"Prioridad {proyecto.prioridad} ID {proyecto.id}" if proyecto.id else "Proyecto nuevo"
            

    def _compute_urgente(self):
        for proyecto in self:
            prio=bool
            if proyecto.prioridad > 7 : prio=True
            else : prio = False
            proyecto.urgente = prio

    def _compute_fecha(self):
        for proyecto in self:
            if proyecto.fecha_creacion:
                proyecto.fecha_creacion + timedelta(fields.Datetime.now())
    
    def _compute_fechaMod(self):
        for proyecto in self:
            if proyecto.fecha_modificacion:
                proyecto.fecha_modificacion + timedelta(fields.Datetime.now())    

class laboratorio(models.Model):
    _name = 'iaangel.laboratorio'
    _description = 'iaangel.laboratorio'

    nombre = fields.Char(required=True)
    pais = fields.Selection([('es','Español'),
                            ('ger','Alemania'),
                            ('eeuu','EE.UU'),
                            ('jap','Japón'),],
                            string="País",
                            help='Seleccione el país')
    
    tipo = fields.Selection([('inv','Investigación'),
                             ('pro','Producción'),
                             ('clo','Cloud'),],
                             string="Tipo",
                             help='Seleccione el tipo'
                             )
    #Un laboratorio puede tener varios proyectos
    proyecto_id = fields.One2many('iaangel.proyecto','laboratorio_id')

class cientifico(models.Model):
    _name = 'iaangel.cientifico'
    _description = 'iaangel.cientifico'

    nombre = fields.Char(required=True)

    #Un cientifico puede tener varios proyectos
    proyecto_id = fields.One2many('iaangel.proyecto','cientifico_id')
    #Un cientifico solo tiene una especialidad
    especialidad_id = fields.Many2one('iaangel.especialidad')

class recurso(models.Model):
    _name = 'iaangel.recurso'
    _description = 'iaangel.recurso'

    nombre = fields.Char(required=True)
    cantidad_disponible = fields.Integer(default=0)

    #Un recurso puede tener varios proyectos
    proyecto_id = fields.Many2many('iaangel.proyecto')

class especialidad(models.Model):
    _name = 'iaangel.especialidad'
    _description = 'iaangel.especialidad'

    nombre = fields.Char(required=True)
    #Una especialidad puede tener varios cientificos
    cientifico_id = fields.One2many('iaangel.cientifico','especialidad_id')
    #Una especialidad puede tener varios proyectos
    proyecto_id = fields.One2many('iaangel.proyecto','especialidad_id')
