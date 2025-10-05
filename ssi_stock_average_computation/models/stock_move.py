# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    stock_average_computation_id = fields.Many2one(
        comodel_name="stock_average_computation.detail",
        string="Stock Average Computation",
        ondelete="set null",
    )
