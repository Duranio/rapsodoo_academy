# Copyright 2021-TODAY Rapsodoo Italia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models,fields,api
from odoo.exceptions import UserError

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

    _sql_constraints = [("license_plate_unique", "UNIQUE(license_plate)", "Warning: license plate already exists!")]

    registration_year = fields.Integer(
        string="Registration Year",
    )

    entry_date = fields.Date(
        string="Entry Date",
        required=True
    )    

    vehicle_type = fields.Selection(
            selection=[("car", "car"),("motocyle", "motocylce")],
            string="Type of Vehicle",
            required=True,
    )

    garage_id = fields.Many2one(
        comodel_name='garage.garage',
        string="Garage"
    )

    #AUTOMATIC CALCULATION OF DAILY FARE
    #Solution 1: compute field + @api.depends("vehicle_type") decorator
    daily_fare = fields.Float(
        string="Daily Fare",
        compute="_compute_daily_fare",
        store=True,
    )
    
    @api.depends("vehicle_type")
    def _compute_daily_fare(self):
        if self.vehicle_type == "car":
            self.daily_fare = 10.0
        else:
            self.daily_fare = 5.0

    '''
    #Solution 2(more flexible): normal field + @api.onchange("vehicle_type") decorator
    daily_fare = fields.Float(
        string="Daily Fare",
    )

    @api.onchange('vehicle_type')
    def onchange_vehicle_type(self):
        if self.vehicle_type == "car":
            self.daily_fare = 10.0
        else:
            self.daily_fare = 5.0
    '''

    #CRUD METHODS
    @api.model
    def create(self, values):
        #Check for max number of vehicle in the garage
        garage = self.env['garage.garage'].search([('id', '=', values["garage_id"])])
        if garage.vehicles_number > garage.vehicles_number_compute:
            #Turn name and license_plate into uppercase
            values["name"] = values["name"].upper()
            values["license_plate"] = values["license_plate"].upper()
            return super(Vehicle, self).create(values)
        else:
            raise UserError("This garage is FULL!!!")

    def write(self, values):
        #Turn name into uppercase
        try:
           values["name"] = values["name"].upper()
        except KeyError:
            #print("KEYERROR EXCEPTION")
            self.name = self.name.upper()

        #Turn license_plate into uppercase
        try:
           values["license_plate"] = values["license_plate"].upper()
        except KeyError:
            #print("KEYERROR EXCEPTION")
            self.license_plate = self.license_plate.upper()
        
        return super(Vehicle, self).write(values)

    def unlink(self):
        for vehicle in self:
            choice = input("Are you sure you want to delete the vehicle {} {} from garage {}? (Type y/n): ".format(vehicle.name, vehicle.license_plate, vehicle.garage_id))
            if choice == "y":
                print("Deleting vehicle {} {}".format(vehicle.name, vehicle.license_plate))
                super(Vehicle, vehicle).unlink()
            else:
                print("Deletion aborted")
        return True