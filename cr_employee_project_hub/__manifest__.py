{
    'name': 'cr_employee_project_hub',
    'version': '1.0',
    'summary': 'cr_employee_project_hub',
    'description': """
        cr_employee_project_hub
    """,
    'category': 'accounting',
    'website': '',
    'depends': ['base', 'hr', 'project'],
    'author': 'dipen',
    'data': [
        'security/ir.model.access.csv',
        'views/employee_training.xml',
        'views/training_session.xml',
        'views/employee_menus.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}