{
    'name': 'cr_product_reviews',
    'version': '1.0',
    'summary': 'Product Reviews Model',
    'description': """
        Product Reviews Model
    """,
    'category': 'accounting',
    'website': '',
    'depends': ['base', 'product'],
    'author': 'dipen',
    'data': [
        'security/ir.model.access.csv',
        'views/product_review.xml',
        # 'views/product_template_view.xml'
        'views/product_product.xml'
    ],
    'demo': [],
    'images': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}