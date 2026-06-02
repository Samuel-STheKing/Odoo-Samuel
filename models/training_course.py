from odoo import models, fields, api

class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Curso de Capacitación'
    _rec_name = 'name'

    name = fields.Char(string='Nombre del Curso', required=True)
    description = fields.Text(string='Descripción del Curso')
    active = fields.Boolean(default=True)

    # Relaciones
    material_ids = fields.One2many('training.material', 'course_id', string='Materiales')
    quiz_ids = fields.One2many('training.quiz', 'course_id', string='Pruebas')

    total_materials = fields.Integer(string='Total Materiales', compute='_compute_totals')
    total_quizzes = fields.Integer(string='Total Pruebas', compute='_compute_totals')

    @api.depends('material_ids', 'quiz_ids')
    def _compute_totals(self):
        for course in self:
            course.total_materials = len(course.material_ids)
            course.total_quizzes = len(course.quiz_ids)

    # === NUEVO MÉTODO PARA PRECARGAR ESTUDIANTES ===
    @api.model
    def default_get(self, fields_list):
        res = super(TrainingCourse, self).default_get(fields_list)
        
        # Verificamos si 'quiz_ids' está en la lista de campos solicitados por la vista
        if 'quiz_ids' in fields_list:
            # Lista de nombres por defecto que deseas que aparezcan
            default_students = [
                "Estudiante 1",
                "Estudiante 2",
                "Estudiante 3",
                "Estudiante 4",
                "Estudiante 5"
            ]
            
            # Usamos el comando ORM (0, 0, {valores}) para crear registros en el One2many de forma virtual
            quiz_lines = []
            for name in default_students:
                quiz_lines.append((0, 0, {
                    'student_name': name,
                    'score_a1': 0.0,
                    'score_a2': 0.0,
                    'score_a3': 0.0,
                    'score_a4': 0.0,
                    'score_a5': 0.0,
                }))
            
            # Asignamos las líneas calculadas al diccionario de valores por defecto
            res.update({
                'quiz_ids': quiz_lines
            })
            
        return res