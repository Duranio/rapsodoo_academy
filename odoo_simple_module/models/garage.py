# Copyright 2021-TODAY Rapsodoo Italia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models,fields,api
from datetime import datetime


class Garage(models.Model):
    numero_di_targa_progressivo = 0

    _name = "garage.garage"
    _description = "Garage Model"

    name = fields.Char(
        string="Name",
        required=True,
    )

    vehicles_number = fields.Integer(
        string="Max Vehicles Number",
        required=True,
    )

    ceiling_height = fields.Float(
        string="Ceiling Height",
    )

    vehicles_number_compute = fields.Integer(
        string="Stored Vehicles",
        compute="_compute_vechicle_numbers",
        store=True,
    )

    start_date = fields.Date(
        string="Start Date"
    )

    date_vehicles_number_change = fields.Date(
        string="Date change number"
    )

    vehicle_ids = fields.One2many(
        comodel_name="vehicle.vehicle",
        inverse_name="garage_id",
        string="Vehicles",
    )

    total_daily_fare = fields.Float(
        string="Total Daily Fare",
        compute="_compute_total_daily_fare",
        store=True,
    )

    @api.depends("vehicle_ids")
    def _compute_vechicle_numbers(self):
        for garage in self:
            value = len(garage.vehicle_ids)
            garage.vehicles_number_compute = value

    @api.depends("vehicles_number_compute")
    def _compute_total_daily_fare(self):
        total = 0.0
        for vehicle in self.vehicle_ids:
            total += vehicle.daily_fare
        self.total_daily_fare = total
    
    @api.onchange('vehicles_number')
    def onchange_vehicle_number(self):
        self.date_vehicles_number_change = fields.Date.today()

    #CRUD METHODS
    @api.model
    def create(self, values):
        print(values)
        values["start_date"] = "1973-01-01"
        return super(Garage, self).create(values)

    def write(self, values):

        now = datetime.now()
        timestamp = datetime.timestamp(now)
        vehicle_values = {
            "name": "Veicolo di prova",
            "license_plate": "TARGA_DI_PROVA_"+str(hex(int(timestamp*1000000)))[2:]
        }
        self.env['vehicle.vehicle'].create(vehicle_values)

        return super(Garage, self).write(values)
                
    def unlink(self):
        #Print to console the list of vehicles currently stored in this garage
        vehicles_in_garage = self.env['vehicle.vehicle'].search([('garage_id', '=', self.id)])
        print("List of vehicles currently stored in the garage", self.name)
        for vehicle in vehicles_in_garage:
            print("Vehicle Name: {} - License Plate: {}".format(vehicle.name, vehicle.license_plate))
                
        '''
        #Code to delete all the vehicles currently stored in this garage
        for vehicle in vehicles_in_garage:
            vehicle.unlink()
        '''
        return super(Garage, self).unlink() 
        
