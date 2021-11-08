# Copyright 2021-TODAY Rapsodoo Italia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models,fields,api


class Vehicle(models.Model):
    _name = 'vehicle.vehicle'
    _description = "Vehicle Model"

    name = fields.Char(
        string="Name",
        required=True,
    )

    license_plate = fields.Char(
        string="License Plate",
        required=True,
    )

    garage_id = fields.Many2one(
        comodel_name='garage.garage',
        string="Garage"
    )

    def unlink(self):
        choice = input("Are you sure you want to delete the vehicle {} {} from garage {}? (Type y/n): ".format(self.name, self.license_plate, self.garage_id))
        if choice == "y":
            print("Deleting vehicle {} {}".format(self.name, self.license_plate))
            return super(Vehicle, self).unlink()
        else:
            print("Deletion aborted")
            return False
