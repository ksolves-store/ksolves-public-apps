# -*- coding: utf-8 -*-
{
    'name': "Stock Access Restriction",

    'summary': """
        Stock Access Restriction v15.0""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ksolves India Pvt. Ltd.",
    'website': "https://store.ksolves.com/",
    'category': 'Stock Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ks_stock_location_extension_view.xml',
        'views/ks_res_users_extension_view.xml',
        'security/security.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],
}
