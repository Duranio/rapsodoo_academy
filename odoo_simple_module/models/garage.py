# Copyright 2021-TODAY Rapsodoo Italia S.r.L. (www.rapsodoo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models,fields,api


class Garage(models.Model):
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
                
    def unlink(self):
        vehicle_ids = self.env['vehicle.vehicle'].search([('garage_id', '=', self.id)])
        print("List of vehicles currently stored in the garage")
        for vehicle in vehicle_ids:
            print(vehicle.name, vehicle.license_plate)
        #Scrivere codice per eliminare i veicoli associati a questo garage.
        #Hint: usare ciclo for su vehicle_ids e metoodo unlink()
        for vehicle in vehicle_ids:
            vehicle.unlink()
        return super(Garage, self).unlink() 
        
