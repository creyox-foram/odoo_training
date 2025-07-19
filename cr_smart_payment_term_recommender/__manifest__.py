# -*- coding: utf-8 -*-
# Part of Creyox Technologies.
{
    'name': 'cr_smart_payment_term_recommender',
    'version': '1.0',
    'summary': 'cr_smart_payment_term_recommender',
    'description': """
        cr_smart_payment_term_recommender
    """,
    'category': 'accounting',
    'website': '',
    'authro': 'Creyox Technologies',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_term_matrix.xml',
        'views/payment_term_matrix_rule.xml',
        'views/payment_term_matrix_rule_line.xml',
        'views/payment_term_mapping_rule.xml',
        'data/payment_term_matrix_data.xml'
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}