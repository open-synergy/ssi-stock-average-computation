# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockAverageComputationType(models.Model):
    _name = "stock_average_computation_type"
    _description = "Stock Average Computation Type"
    _inherit = [
        "mixin.master_data",
        "mixin.product_category_m2o_configurator",
        "mixin.product_product_m2o_configurator",
    ]

    _product_category_m2o_configurator_insert_form_element_ok = True
    _product_category_m2o_configurator_form_xpath = "//page[@name='product']"
    _product_product_m2o_configurator_insert_form_element_ok = True
    _product_product_m2o_configurator_form_xpath = "//page[@name='product']"
