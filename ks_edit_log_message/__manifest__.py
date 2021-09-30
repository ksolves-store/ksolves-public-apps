# -*- coding: utf-8 -*-
{
    'name': "Edit Log Message",

    'summary': """This Module provide user can edit and delete messages""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ksolves India Ltd.",
    'website': "http://www.ksolves.com",
    'category': 'Tools',
    'version': '14.0.0.0.0',
    'maintainer': 'Ksolves India Ltd.',
    'support': 'sales@ksolves.com',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sales_team','mail'],

    # always loaded
    'data': [
        'security/ks_group_access.xml',
        'views/ks_mail_message_inherit.xml',
        'views/ks_assets.xml',
    ],
'qweb': [
        "static/src/xml/ks_custom_message.xml",
],

}
