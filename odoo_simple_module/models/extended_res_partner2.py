from odoo import models,fields,api


class Extended_Res_Partner2(models.Model):
    _name="extended.res.partner2"
    _inherit="res.partner"
    _description="Extended Res Partner2"

    
    vehicles = fields.One2many(
        comodel_name="vehicle.vehicle",
        inverse_name="extended_res_partner2_id",
        string="Vehicles",
    )

    channel_ids = fields.Integer(
        string="channel ids"
    )

    meeting_ids = fields.Integer(
        string="meeting ids"
    )
