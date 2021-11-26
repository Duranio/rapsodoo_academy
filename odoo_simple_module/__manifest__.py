# Copyright 2021-TODAY Rapsodoo Italia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': "Garage",
    'version': '14.0.1.0.0',
    'depends': [
        'base',
    ],
    'author': "Fabio Caputi",
    'category': 'Category',
    'description': 'Inheritance Test Module',
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/garage_views.xml',
        'views/vehicle_views.xml',
        'views/extended_res_partner_views.xml',
        'views/templates.xml',
    ],
}
