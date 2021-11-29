# Copyright 2021-TODAY Rapsodoo Italia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models,fields,api
from odoo.exceptions import UserError
import random

class Vehicle(models.Model):
    _name = 'vehicle.vehicle'
    _description = "Vehicle Model"

    name = fields.Char(
        string="Name",
        required=True,
    )

    car_image = fields.Binary("Image")
    color = fields.Integer(
        string="Rough Color"
    )

    color_string = fields.Char(
        string="Exact Color"
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
    )    

    vehicle_type = fields.Selection(
            selection=[("car", "car"),("motocyle", "motocylce")],
            string="Type of Vehicle",
    )

    garage_id = fields.Many2one(
        comodel_name='garage.garage',
        string="Garage"
    )
    
    extended_res_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner"
    )

    extended_res_partner2_id = fields.Many2one(
        comodel_name='extended.res.partner2',
        string="Partner"
    )
    

    #AUTOMATIC CALCULATION OF DAILY FARE
    #Solution 1: compute field + @api.depends("vehicle_type") decorator
    daily_fare = fields.Float(
        string="Daily Fare",
        compute="_compute_daily_fare",
        store=True,
    )
    
    def show_message_to_console(self):
        print("MESSAGGIO INUTILE")

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

        #calculating next vehicle id
        self.env.cr.execute("SELECT MAX(id) FROM vehicle_vehicle")
        record = self.env.cr.fetchone()            
        max_id = record[0] + 1

        #generate a random string
        name = str(max_id)+"_"
        for i in range(random.randrange(5,12)):
            name += chr(random.randrange(65,90))
        owner_values = {
            "name": name,               
        }        

        #create a res partner object with a random name
        owner = self.env['res.partner'].create(owner_values)

        #assign this vehicle to the new res partner object created above
        values["extended_res_partner_id"] = owner.id

        #Check for max number of vehicle in the garage
        if 'garage_id' in values.keys():
            garage = self.env['garage.garage'].search([('id', '=', values["garage_id"])])
            if garage.vehicles_number > garage.vehicles_number_compute:
                #Turn name and license_plate into uppercase
                values["name"] = values["name"].upper()
                values["license_plate"] = values["license_plate"].upper()
                return super(Vehicle, self).create(values)
            else:
                raise UserError("This garage is FULL!!!")
        else:
            
            return super(Vehicle, self).create(values) 

    def write(self, values):
        
        #Turn name into uppercase    
        if "name" in values.keys():
           values["name"] = values["name"].upper()
        
        #Turn license_plate into uppercase        
        if "license_plate" in values.keys():
           values["license_plate"] = values["license_plate"].upper()
       
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