from odoo import models, fields, api
from datetime import timedelta

class Project(models.Model):
    _name = 'manage.project'
    _description = 'Project'

    name = fields.Char(required=True)
    description = fields.Char()
    history_ids = fields.One2many('manage.history', 'project_id')
    sprint_ids = fields.One2many('manage.sprint', 'project_id')

    code = fields.Char(compute="_compute_code", store=True)

    @api.depends('id')
    def _compute_code(self):
        for project in self:
            project.code = f"PROY_{project.id or 0}"


class Sprint(models.Model):
    _name = 'manage.sprint'
    _description = 'Sprint'

    name = fields.Char(required=True)
    description = fields.Char()
    duration = fields.Integer()
    startdate = fields.Datetime()
    enddate = fields.Datetime(compute="_compute_enddate", store=True)
    project_id = fields.Many2one('manage.project')
    task_ids = fields.One2many('manage.task', 'sprint_id')

    @api.depends('startdate', 'duration')
    def _compute_enddate(self):
        for sprint in self:
            if sprint.startdate and sprint.duration:
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

    used_technologies = fields.Many2many(
        "manage.technology",
        compute="_compute_used_technologies",
        store=True
    )

    @api.depends('task_ids', 'task_ids.technology_ids')
    def _compute_used_technologies(self):
        for history in self:
            technologies = self.env['manage.technology']
            for task in history.task_ids:
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
    sprint_id = fields.Many2one('manage.sprint', compute='_compute_sprint', store=True)
    technology_ids = fields.Many2many('manage.technology')
    # campo relacionado que refleja el proyecto de la historia
    project_id = fields.Many2one('manage.project', related='history_id.project_id', readonly=True, store=True)

    code = fields.Char(compute="_compute_code", store=True)

    @api.depends('id')
    def _compute_code(self):
        for task in self:
            # Código de tarea, cámbialo si prefieres otro formato
            task.code = f"TASK_{task.id or 0}"

    @api.depends('history_id', 'history_id.project_id', 'history_id.project_id.sprint_ids.enddate')
    def _compute_sprint(self):
        for task in self:
            if not task.history_id or not task.history_id.project_id:
                task.sprint_id = False
                continue

            sprint = self.env['manage.sprint'].search([
                ('project_id', '=', task.history_id.project_id.id),
                ('enddate', '>', fields.Datetime.now())
            ], limit=1)

            task.sprint_id = sprint.id if sprint else False


class Technology(models.Model):
    _name = 'manage.technology'
    _description = 'Technology'

    name = fields.Char(required=True)
    description = fields.Char()
    photo = fields.Image()
    task_ids = fields.Many2many('manage.task')
