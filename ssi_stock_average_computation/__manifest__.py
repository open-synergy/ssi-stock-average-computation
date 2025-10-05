# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "SSI Stock Average Computation",
    "version": "14.0.1.0.0",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "website": "https://github.com/open-synergy/ssi-stock-average-computation",
    "license": "AGPL-3",
    "depends": [
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_stock",
        "ssi_m2o_configurator_mixin",
        "queue_job_batch",
    ],
    "data": [
        "security/res_group.xml",
        "security/ir_model_access.xml",
        "security/ir_module_category/stock_average_computation.xml",
        "security/res_groups/stock_average_computation.xml",
        "security/ir_model_access/stock_average_computation.xml",
        "security/ir_model_access/product_average_computation.xml",
        "security/ir_rule/stock_average_computation.xml",
        "ir_sequence/stock_average_computation.xml",
        "sequence_template/stock_average_computation.xml",
        "policy_template/stock_average_computation.xml",
        "approval_template/stock_average_computation.xml",
        "data/ir_actions_server_data.xml",
        "data/base_automation_data.xml",
        "menu.xml",
        "views/product_product.xml",
        "views/stock_average_computation_type.xml",
        "views/stock_average_computation.xml",
    ],
    "demo": [],
    "application": False,
    "installable": True,
    "auto_install": False,
}
