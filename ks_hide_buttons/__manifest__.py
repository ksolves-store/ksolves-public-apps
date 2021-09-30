# -*- coding: utf-8 -*-
{
    'name': "Hide Edit Create Buttons",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ks_hide_groups.xml',
        'views/ks_assets.xml',
        'views/ks_hide_button.xml',
    ],
}
