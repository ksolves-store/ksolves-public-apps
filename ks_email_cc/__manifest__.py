# -*- coding: utf-8 -*-
{
    'name': "Email CC",

    'summary': """
        
        """,

    'description': """
    """,

    'author': "Ksolves India Ltd.",
    'website': "https://www.ksolves.com/",
    # 'category': 'Tools',
    'license': 'OPL-1',
    'currency': 'USD',
    # 'price': 148.2,
    # "live_test_url":  "http://saastoolkit.kappso.in/",
    'version': '14.0.1.0.0',
    'maintainer': 'Ksolves India Ltd.',
    'support': 'sales@ksolves.com',
    'installable': True,
    'application': True,
    'sequence': 1,
    'depends': ['base','web','mail'],
    'images': [

    ],
    'data': [
        'wizard/ks_message_compose_inherit.xml',
        'views/ks_res_company_inherit.xml',
        'views/ks_web_assets.xml'
    ],

    'qweb': [
           'static/src/xml/ks_templates_inherit.xml',
    ],

}
