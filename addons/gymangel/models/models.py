# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime
import random

# 1. MODELO SOCIO (HERENCIA DE RES.PARTNER)
class GymMember(models.Model):
    _inherit = 'res.partner'

    is_gym_member = fields.Boolean(string="¿Es Socio?", default=False, help="Marcar si esta persona es socio del gimnasio")
    is_instructor = fields.Boolean(string="¿Es Monitor?", default=False, help="Marcar si trabaja como monitor")
    
    # [Rubrica: Relacion One2many]
    booking_ids = fields.One2many('gym.booking', 'member_id', string="Reservas")


# 2. MODELO EQUIPAMIENTO
class GymEquipment(models.Model):
    _name = 'gym.equipment'
    _description = 'Equipamiento del Gimnasio'

    name = fields.Char(string="Nombre Material", required=True, help="Ej: Pesas, Esterilla, Bicicleta")
    quantity = fields.Integer(string="Cantidad Disponible", default=1)
    
    # [Rubrica: Relacion Many2many]
    activity_ids = fields.Many2many(comodel_name="gym.activity",
                                    relation="gym_activity_equipment_rel",
                                    column1="equipment_id",
                                    column2="activity_id",
                                    string="Actividades Relacionadas")


# 3. MODELO ACTIVIDAD
class GymActivity(models.Model):
    _name = 'gym.activity'
    _description = 'Tipo de Actividad'

    name = fields.Char(string="Nombre Actividad", required=True, help="Ej: Yoga, Zumba, Boxeo")
    description = fields.Text(string="Descripción")
    
    equipment_ids = fields.Many2many(comodel_name="gym.equipment",
                                     relation="gym_activity_equipment_rel",
                                     column1="activity_id",
                                     column2="equipment_id",
                                     string="Material Necesario")


# 4. MODELO SESIÓN (CLASE)
class GymSession(models.Model):
    _name = 'gym.session'
    _description = 'Sesión Programada'

    name = fields.Char(string="Identificador Sesión", compute="_get_name", store=True)
    
    start_date = fields.Datetime(string="Fecha Inicio", required=True, default=fields.Datetime.now)
    duration = fields.Integer(string="Duración (min)", default=60, help="Duración en minutos")
    
    # [Rubrica: Campo computado almacenado]
    end_date = fields.Datetime(string="Fecha Fin", compute="_get_end_date", store=True)
    
    capacity = fields.Integer(string="Capacidad Máxima", default=10)
    
    # [Rubrica: Relaciones Many2one y One2many]
    activity_id = fields.Many2one("gym.activity", string="Actividad", required=True)
    instructor_id = fields.Many2one("res.partner", string="Instructor", domain="[('is_instructor', '=', True)]")
    booking_ids = fields.One2many("gym.booking", "session_id", string="Asistentes")
    
    # [Rubrica: Campos computados avanzados]
    occupied_seats = fields.Integer(string="Ocupadas", compute="_get_seats", store=True)
    available_seats = fields.Integer(string="Libres", compute="_get_seats", store=True)
    occupied_percentage = fields.Float(string="Porcentaje Ocupación", compute="_get_seats", store=True)
    
    color = fields.Integer(string="Color Kanban") # Necesario para la vista Kanban

    @api.depends('activity_id', 'start_date')
    def _get_name(self):
        for session in self:
            if session.activity_id and session.start_date:
                session.name = str(session.activity_id.name) + " - " + str(session.start_date)
            else:
                session.name = "Nueva Sesión"

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for session in self:
            if session.start_date and session.duration:
                # Usamos timedelta para sumar minutos
                session.end_date = session.start_date + datetime.timedelta(minutes=session.duration)
            else:
                session.end_date = False

    @api.depends('booking_ids', 'capacity')
    def _get_seats(self):
        for session in self:
            session.occupied_seats = len(session.booking_ids)
            session.available_seats = session.capacity - session.occupied_seats
            if session.capacity > 0:
                session.occupied_percentage = (session.occupied_seats / session.capacity) * 100
            else:
                session.occupied_percentage = 0.0
    
    def f_create_prueba(self):
        # [Rubrica: ORM Create]
        sesion = {
            "name": "Clase de Prueba Generada",
            "capacity": 20,
            "duration": 90
        }
        print("Creando sesión desde código:", sesion)
        self.env['gym.session'].create(sesion)

    def f_search_update(self):
        # [Rubrica: ORM Search y Write]
        sesion = self.env['gym.session'].search([('capacity', '=', 10)], limit=1)
        print('Sesión encontrada:', sesion.name)
        sesion.write({
            "capacity": 15
        })


# 5. MODELO RESERVA
class GymBooking(models.Model):
    _name = 'gym.booking'
    _description = 'Reserva de Plaza'

    code = fields.Char(string="Código Reserva", readonly=True, default="BORRADOR")
    
    # [Rubrica: Lambda Default]
    booking_date = fields.Datetime(string="Fecha Reserva", default=lambda self: fields.Datetime.now())
    
    session_id = fields.Many2one("gym.session", string="Clase", required=True)
    member_id = fields.Many2one("res.partner", string="Socio", required=True, domain="[('is_gym_member', '=', True)]")
    
    state = fields.Selection([('draft', 'Pendiente'),
                              ('confirmed', 'Confirmada'),
                              ('cancelled', 'Cancelada')],
                             string="Estado",
                             default='draft')

    @api.model
    def create(self, vals):
        if vals.get('code', 'BORRADOR') == 'BORRADOR':
            vals['code'] = 'RES-' + str(random.randint(1000, 9999))
        return super(GymBooking, self).create(vals)

    @api.constrains('session_id')
    def _check_capacity(self):
        for booking in self:
            if booking.session_id.available_seats < 0:
                raise ValidationError("¡Error! No quedan plazas libres en esta clase.")

    def action_confirm(self):
        for booking in self:
            booking.state = 'confirmed'