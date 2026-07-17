# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockAverageComputation(models.Model):  # pylint: disable=too-few-public-methods
    _name = "stock_average_computation"
    _inherit = [
        "stock_average_computation",
        "mixin.single_operating_unit",
    ]
