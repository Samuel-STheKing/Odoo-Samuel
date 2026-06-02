# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TrainingQuiz(models.Model):
    _name = 'training.quiz'
    _description = 'Evaluación de Estudiantes (Simulador)'
    _rec_name = 'student_name'
    _order = 'sequence, id'

    course_id = fields.Many2one('training.course', string='Curso', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Orden', default=10)
    
    student_name = fields.Char(string='Estudiante a Evaluar', required=True, placeholder="Ej. Juan Pérez")
    case_description = fields.Text(string='Contexto / Caso del Estudiante', placeholder="Describe el rendimiento o entregables del alumno...")

    # Criterios de Calificación (0 a 20)
    score_a1 = fields.Float(string='Nota A1', default=0.0)
    score_a2 = fields.Float(string='Nota A2', default=0.0)
    score_a3 = fields.Float(string='Nota A3', default=0.0)
    score_a4 = fields.Float(string='Nota A4', default=0.0)
    score_a5 = fields.Float(string='Nota A5', default=0.0)

    # Estados individuales calculados de forma dinámica
    status_a1 = fields.Html(string='Estado A1', compute='_compute_individual_statuses')
    status_a2 = fields.Html(string='Estado A2', compute='_compute_individual_statuses')
    status_a3 = fields.Html(string='Estado A3', compute='_compute_individual_statuses')
    status_a4 = fields.Html(string='Estado A4', compute='_compute_individual_statuses')
    status_a5 = fields.Html(string='Estado A5', compute='_compute_individual_statuses')

    final_average = fields.Float(string='Promedio Final', compute='_compute_quiz_results', store=True)
    state = fields.Selection([
        ('fail', 'Desaprobado'),
        ('pass', 'Aprobado')
    ], string='Estado de la Evaluación', compute='_compute_quiz_results', store=True)

    @api.depends('score_a1', 'score_a2', 'score_a3', 'score_a4', 'score_a5')
    def _compute_individual_statuses(self):
        badge_pass = '<span style="color: #28a745; font-weight: bold; margin-left: 10px;">✅ Aprobado</span>'
        badge_fail = '<span style="color: #dc3545; font-weight: bold; margin-left: 10px;">❌ Reprobado</span>'
        
        for record in self:
            record.status_a1 = badge_pass if record.score_a1 >= 12.0 else badge_fail
            record.status_a2 = badge_pass if record.score_a2 >= 12.0 else badge_fail
            record.status_a3 = badge_pass if record.score_a3 >= 12.0 else badge_fail
            record.status_a4 = badge_pass if record.score_a4 >= 12.0 else badge_fail
            record.status_a5 = badge_pass if record.score_a5 >= 12.0 else badge_fail

    @api.depends('score_a1', 'score_a2', 'score_a3', 'score_a4', 'score_a5')
    def _compute_quiz_results(self):
        for record in self:
            total = record.score_a1 + record.score_a2 + record.score_a3 + record.score_a4 + record.score_a5
            average = total / 5.0
            record.final_average = round(average, 2)
            
            if record.final_average >= 12.0:
                record.state = 'pass'
            else:
                record.state = 'fail'