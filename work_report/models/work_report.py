from odoo import models, fields, api

class WorkArea(models.Model):
    _name = 'work.area'
    _description = 'Área de Trabajo'
    _order = 'name'

    name = fields.Char(string='Área', required=True)
    active = fields.Boolean(default=True)

    @api.onchange('name')
    def _onchange_name_upper(self):
        if self.name:
            self.name = self.name.upper()

    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()
        return super(WorkArea, self).create(vals)

    def write(self, vals):
        if 'name' in vals and vals['name']:
            vals['name'] = vals['name'].upper()
        return super(WorkArea, self).write(vals)


class WorkReport(models.Model):
    _name = 'work.report'
    _description = 'Work Report'
    _order = 'create_date desc'

    name = fields.Char(
        string='Código',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default='Nuevo', 
    )
    title = fields.Char(string='Título del Reporte', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('sent', 'Enviado'),
    ], string='Estado', default='draft', required=True, readonly=True, copy=False)

    area_id = fields.Many2one(
        'work.area',
        string='Área',
        required=True,
        index=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Usuario',
        default=lambda self: self.env.user,
        readonly=True,
        required=True,
    )
    date = fields.Date(
        string='Fecha',
        default=fields.Date.context_today,
        readonly=True,
        required=True,
        index=True,
    )
    message = fields.Text(string='Reporte / Mensaje', required=True)
    submission_time = fields.Datetime(string='Hora de Envío', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('work.report') or 'Nuevo'
        return super(WorkReport, self).create(vals)

    def action_send(self):
        """Cambia el estado a Enviado y registra la fecha/hora exacta"""
        for record in self:
            if record.state == 'draft':
                record.write({
                    'state': 'sent',
                    'submission_time': fields.Datetime.now()
                })

    def action_save_draft(self):
        """
        Método dummy para el botón 'Guardar Borrador'. 
        Simplemente refresca la vista guardando los datos del formulario.
        """
        return True