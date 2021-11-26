from odoo import models,fields,api


class Extended_Res_Partner(models.Model):
    #_name="extended.res.partner"
    _inherit="res.partner"
    _description="Extended Res Partner"

    
    vehicles = fields.One2many(
        comodel_name="vehicle.vehicle",
        inverse_name="extended_res_partner_id",
        string="Vehicles",
    )
    