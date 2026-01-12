from odoo import models, fields, api
from datetime import timedelta # ### IMPRESCINDIBLE para sumar/restar fechas

class Project(models.Model):
    _name = 'manage.project'
    _description = 'Project'

    name = fields.Char(required=True) # ### required=True hace el campo obligatorio (línea azul en la vista)
    description = fields.Char()
    
    # ### RELACIONES ONE2MANY
    # Estructura: fields.One2many('modelo.hijo', 'campo_en_el_hijo_que_apunta_aqui')
    history_ids = fields.One2many('manage.history', 'project_id')
    sprint_ids = fields.One2many('manage.sprint', 'project_id')

    # ### CAMPO CALCULADO (NO ALMACENADO)
    # store=False: Se calcula cada vez que lo miras. No se guarda en BBDD.
    # Ideal para mostrar información dinámica.
    code = fields.Char(compute="_compute_code", store=False)

    def _compute_code(self):
        for project in self:
            # ### OJO: project.id puede no existir si estás creando uno nuevo.
            # Usamos un if ternario para evitar errores.
            project.code = f"PROY_{project.id}" if project.id else "PROY_NUEVO"


class Sprint(models.Model):
    _name = 'manage.sprint'
    _description = 'Sprint'

    name = fields.Char(required=True)
    description = fields.Char()
    duration = fields.Integer()
    startdate = fields.Datetime()
    
    # ### CAMPO CALCULADO (ALMACENADO)
    # store=True: Se calcula y SE GUARDA en BBDD. Solo se recalcula si cambian
    # los campos del @api.depends. Necesario si quieres buscar/filtrar por este campo.
    enddate = fields.Datetime(compute="_compute_enddate", store=True)
    
    # ### RELACIÓN MANY2ONE (La contraparte del One2many)
    project_id = fields.Many2one('manage.project')
    task_ids = fields.One2many('manage.task', 'sprint_id')

    @api.depends('startdate', 'duration') # ### DECORADOR OBLIGATORIO
    def _compute_enddate(self):
        for sprint in self:
            # Siempre verifica que tienes datos antes de operar
            if sprint.startdate and sprint.duration:
                # ### ARITMÉTICA DE FECHAS: Fecha + timedelta(días/horas)
                sprint.enddate = sprint.startdate + timedelta(days=sprint.duration)
            else:
                sprint.enddate = False


class History(models.Model):
    _name = 'manage.history'
    _description = 'User Story'

    name = fields.Char(required=True)
    description = fields.Char()
    project_id = fields.Many2one('manage.project')
    task_ids = fields.One2many('manage.task', 'history_id')

    # ### MANY2MANY CALCULADO
    used_technologies = fields.Many2many(
        "manage.technology",
        compute="_compute_used_technologies",
        store=True
    )

    # ### RECORRER RELACIONES
    # Dependemos de las tareas y de las tecnologías DE esas tareas
    @api.depends('task_ids', 'task_ids.technology_ids')
    def _compute_used_technologies(self):
        for history in self:
            # Creamos un recordset vacío del modelo destino
            technologies = self.env['manage.technology']
            for task in history.task_ids:
                # ### OPERADOR |= (Unión de conjuntos)
                # Añade las tecnologías de la tarea al conjunto total sin duplicados
                technologies |= task.technology_ids
            history.used_technologies = technologies


class Task(models.Model):
    _name = 'manage.task'
    _description = 'Task'

    name = fields.Char(required=True)
    description = fields.Char()
    startdate = fields.Datetime()
    enddate = fields.Datetime()
    ispaused = fields.Boolean()
    
    history_id = fields.Many2one('manage.history')
    
    # ### MANY2ONE CALCULADO AUTOMÁTICAMENTE
    # Esto asigna la tarea a un sprint automáticamente según reglas
    sprint_id = fields.Many2one('manage.sprint', compute='_compute_sprint', store=True)
    
    technology_ids = fields.Many2many('manage.technology')
    
    # ### CAMPO RELATED (Campo espejo)
    # Muestra un dato que está en otra tabla.
    # related='campo_relacional.campo_que_queremos'
    # readonly=True es buena práctica porque no deberías editarlo aquí.
    project_id = fields.Many2one('manage.project', related='history_id.project_id', readonly=True, store=True)

    code = fields.Char(compute="_compute_code", store=False)

    def _compute_code(self):
        for task in self:
            task.code = f"TASK_{task.id}" if task.id else "TASK_NUEVO"

    # ### LÓGICA DE NEGOCIO COMPLEJA (SEARCH)
    @api.depends('history_id', 'history_id.project_id', 'history_id.project_id.sprint_ids.enddate')
    def _compute_sprint(self):
        for task in self:
            # 1. Clausulas de guarda: Si faltan datos base, limpiamos y saltamos
            if not task.history_id or not task.history_id.project_id:
                task.sprint_id = False
                continue

            # 2. BÚSQUEDA EN BBDD (self.env[modelo].search)
            # Sintaxis: [('campo', 'operador', 'valor'), (...)]
            sprint = self.env['manage.sprint'].search([
                ('project_id', '=', task.history_id.project_id.id), # Del mismo proyecto
                ('enddate', '>', fields.Datetime.now())             # Que no haya caducado
            ], limit=1) # limit=1 nos devuelve solo el primero que encuentre

            # Asignamos el ID si encontramos algo
            task.sprint_id = sprint.id if sprint else False


class Technology(models.Model):
    _name = 'manage.technology'
    _description = 'Technology'

    name = fields.Char(required=True)
    description = fields.Char()
    photo = fields.Image() # ### Campo Image para fotos pequeñas
    task_ids = fields.Many2many('manage.task')


# ### HERENCIA (INHERIT)
# Fundamental para modificar módulos existentes sin romperlos
class Developer(models.Model):
    _inherit = 'res.partner' # ### Heredamos de CONTACTOS (res.partner)

    # Añadimos campos nuevos a la tabla existente
    technologies = fields.Many2many(
        'manage.technology',
        relation='developer_technologies', # Nombre tabla intermedia opcional
        column1='developer_id',
        column2='technologies_id',
        string='Tecnologías'
    )

    is_dev = fields.Boolean(string="¿Es desarrollador?", default=False)