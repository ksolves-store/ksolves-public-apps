{
    'name': "Calculator",
    'summary': """Calculator within the odoo framework""",
    'description': """Calculator within the odoo framework. Allows for multiple calculations. 
    """,
    'version': '14.0.0.0.0',
    'category': 'Tools',
    'license': 'LGPL-3',
    'author': "Ksolves India Ltd.",
    'maintainer': 'Ksolves India Ltd.',
    'support': 'sales@ksolves.com',
    'website': "https://www.ksolves.com/",
    'depends': [
        'base',
        'web'
    ],
    'data': [
        'views/ks_assets.xml',
    ],
    'qweb': ['static/src/xml/ks_calculator.xml'],

    'installable': True,
    'application': False,
    'auto_install': False,
}