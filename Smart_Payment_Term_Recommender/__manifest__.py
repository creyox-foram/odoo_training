# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
{
    'name': 'Smart_Payment_Term_Recommender',
    'version': '1.0',
    'summary': 'Smart Payment Term Recommender',
    'description': """
        Smart Payment Term Recommender
    """,
    'category': 'accounting',
    'website': '',
    'authro': 'Creyox Technologies',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_term_matrix.xml',
        'views/payment_term_matrix_rule.xml',
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}