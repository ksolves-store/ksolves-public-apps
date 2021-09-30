# -*- coding: utf-8 -*-
{
    'name': "Product Price List",

    'summary': """This module helps to user see details in sale order lines  """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Ksolves India Ltd.",
    'website': "http://www.ksolves.com",
    'category': 'Tools',
    'version': '14.0.0.0.0',
    'maintainer': 'Ksolves India Ltd.',
    'support': 'sales@ksolves.com',
    'category': 'Tools',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/ks_price_list.xml',
        'views/ks_product_inherit.xml',
        'views/ks_assets.xml',
        'static/xml/ks_print_unit_widget.xml'
    ],
    # only loaded in demonstration mode
    'qweb': [
        'static/xml/ks_price_template.xml',
    ],
}
