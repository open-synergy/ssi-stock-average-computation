# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = "product.product"

    average_computation_ids = fields.One2many(
        comodel_name="stock_average_computation.detail",
        inverse_name="product_id",
        string="Average Computations",
    )
    latest_average_computation_id = fields.Many2one(
        comodel_name="stock_average_computation.detail",
        string="Latest Average Computation",
        compute="_compute_latest_average_computation_date",
        store=True,
    )
    latest_average_computation_date = fields.Datetime(
        string="Latest Average Computation Date",
        compute="_compute_latest_average_computation_date",
        store=True,
    )

    @api.depends(
        "average_computation_ids.latest_average_computation_date",
        "average_computation_ids",
        "average_computation_ids.stock_average_computation_id.state",
    )
    def _compute_latest_average_computation_date(self):
        for record in self:
            if (
                len(
                    record.average_computation_ids.filtered(
                        lambda r: r.stock_average_computation_id.state == "done"
                    )
                )
                > 0
            ):
                latest_average_computation = record.average_computation_ids.filtered(
                    lambda r: r.stock_average_computation_id.state == "done"
                )[0]
                record.latest_average_computation_id = latest_average_computation
                record.latest_average_computation_date = (
                    latest_average_computation.date_cutoff
                )
