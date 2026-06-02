{
    'name': 'School Training - Elearning',
    'version': '16.0.1.0.0',
    'category': 'Education',
    'summary': 'Capacitación con videos, documentos y pruebas',
    'description': """
        Módulo de e-learning que permite subir contenido audiovisual y documentos,
        y realizar pruebas para verificar el aprendizaje.
    """,
    'author': 'Tu Nombre',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/training_course_views.xml',
        'views/training_material_views.xml',
        'views/training_quiz_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}