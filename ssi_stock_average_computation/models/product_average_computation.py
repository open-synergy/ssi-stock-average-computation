# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductAverageComputation(models.Model):
    _name = "product.average_computation"
    _description = "Product - Average Computation"
    _order = "product_id, latest_average_computation_date desc"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
    )
    latest_average_computation_date = fields.Datetime(
        string="Latest Average Computation Date",
    )
    latest_average_cost = fields.Float(
        string="Latest Average Cost",
    )
    latest_quantity = fields.Float(
        string="Latest Quantity",
    )
    latest_value = fields.Float(
        string="Latest Value",
        compute="_compute_latest_value",
        store=True,
    )

    @api.depends("latest_average_cost", "latest_quantity")
    def _compute_latest_value(self):
        for record in self:
            record.latest_value = record.latest_average_cost * record.latest_quantity
