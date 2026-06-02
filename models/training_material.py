from odoo import models, fields, api

class TrainingMaterial(models.Model):
    _name = 'training.material'
    _description = 'Material de Aprendizaje'
    _order = 'sequence, id'

    name = fields.Char(string='Título del Material', required=True)
    course_id = fields.Many2one(
        'training.course',
        string='Curso',
        required=True,
        ondelete='cascade'
    )

    material_type = fields.Selection([
        ('video',    'Video'),
        ('audio',    'Audio'),
        ('pdf',      'Documento PDF'),
        ('document', 'Documento'),
        ('text',     'Texto / HTML'),
    ], string='Tipo de Material', required=True, default='video')

    file = fields.Binary(string='Archivo', attachment=True)
    file_name = fields.Char(string='Nombre del Archivo')
    
    # Campo computado para inyectar la URL del controlador de Streaming
    file_url = fields.Char(
        compute='_compute_file_url', 
        string='URL del Archivo', 
        compute_sudo=True,  # Fuerza el cálculo correcto de la URL sin problemas de permisos
        store=False         # Al no guardarse en base de datos, se recalcula dinámicamente cada vez que abres el registro
    )

    content_text = fields.Html(string='Contenido (Texto/HTML)')
    description = fields.Text(string='Descripción')
    duration = fields.Integer(string='Duración (minutos)')
    sequence = fields.Integer(string='Orden', default=10)
    allow_download = fields.Boolean(string='Permitir Descarga', default=True)

    @api.depends('file', 'file_name')
    def _compute_file_url(self):
        for record in self:
            # Captura de forma segura si el ID es real y entero (evita los IDs virtuales de ventanas emergentes)
            current_id = record._origin.id if hasattr(record, '_origin') else record.id
            
            if current_id and not isinstance(current_id, models.NewId) and record.file:
                record.file_url = f'/training/stream/{current_id}'
            else:
                record.file_url = False