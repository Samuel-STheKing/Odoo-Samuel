{
    'name': 'Work Report',
    'version': '16.0.1.0.0',
    'summary': 'Módulo de reportes de trabajo diarios',
    'category': 'Human Resources',
    'author': 'Tu Empresa',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/work_report_views.xml',
    ],
    'installable': True,
    'application': True,
}