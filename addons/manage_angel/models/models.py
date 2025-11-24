from odoo import models, fields, api
import datetime

class Project(models.Model):
    _name = 'manage.project'
    _description = 'Project'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    history_ids = fields.One2many('manage.history', 'project_id', string='User Stories')
    sprint_ids = fields.One2many('manage.sprint', 'project_id', string='Sprints')

class Sprint(models.Model):
    _name = 'manage.sprint'
    _description = 'Sprint'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    duration = fields.Integer()
    startdate = fields.Datetime(string='Start Date')
    enddate = fields.Datetime(compute="_get_end_date", store=True, string='End Date')
    project_id = fields.Many2one('manage.project', string='Project')
    task_ids = fields.One2many('manage.task', 'sprint_id', string='Tasks')

    @api.depends('startdate','duration')
    def _get_end_date(self):
        for Sprint in self:
            #try:
                if isinstance(Sprint.startdate, datetime.datetime) and Sprint.duration > 0:
                     Sprint.enddate = Sprint.startdate + datetime.timedelta(days=Sprint.duration)
                else:
                     Sprint.enddate = Sprint.startdate

class History(models.Model):
    _name = 'manage.history'
    _description = 'User Story (History)'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    project_id = fields.Many2one('manage.project', string='Project')
    task_ids = fields.One2many('manage.task', 'history_id', string='Tasks')

class Task(models.Model):
    _name = 'manage.task'
    _description = 'Task'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    startdate = fields.Datetime(string='Start Date')
    enddate = fields.Datetime(string='End Date')
    ispaused = fields.Boolean(string='Is Paused')
    history_id = fields.Many2one('manage.history', string='User Story')
    sprint_id = fields.Many2one('manage.sprint', string='Sprint')
    technology_ids = fields.Many2many('manage.technology', string='Technologies')

class Technology(models.Model):
    _name = 'manage.technology'
    _description = 'Technology'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    photo = fields.Image(string='Photo')
    task_ids = fields.Many2many('manage.task', string='Tasks')
