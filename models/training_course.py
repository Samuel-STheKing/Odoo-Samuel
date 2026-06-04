# -*- coding: utf-8 -*-
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

    # === MÉTODO DEF INITIVO PARA GUARDAR Y REFRESCAR SIN DUPLICAR MIGA DE PAN ===
    def action_save_guide(self):
        """
        Guarda los datos en base de datos y refresca la pantalla actual de forma
        limpia usando el target 'main', evitando que se dupliquen las migas de pan.
        """
        self.ensure_one()
        
        # Retornamos una acción que recarga la misma vista del registro actual de forma nativa
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'main',  # Evita que se acumule el historial en las migas de pan
        }

    # === MÉTODO PARA PRECARGAR ESTUDIANTES ===
    @api.model
    def default_get(self, fields_list):
        res = super(TrainingCourse, self).default_get(fields_list)
        
        if 'quiz_ids' in fields_list:
            default_students = [
                "Estudiante 1",
                "Estudiante 2",
                "Estudiante 3",
                "Estudiante 4",
                "Estudiante 5"
            ]
            
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
            
            res.update({
                'quiz_ids': quiz_lines
            })
            
        return res