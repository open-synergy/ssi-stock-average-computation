# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class StockAverageComputation(models.Model):
    _name = "stock_average_computation"
    _description = "Stock Average Computation"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.many2one_configurator",
    ]
    # mixin.multiple_approval attributes
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve",
        "action_reject",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
        "action_recompute_all_fields",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_done",
        "dom_cancel",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda r: r._default_date(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ]
        },
        help="Date of the stock average computation.",
    )
    date_end = fields.Datetime(
        string="Cutoff Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ]
        },
        help="End date of the stock average computation.",
    )
    type_id = fields.Many2one(
        comodel_name="stock_average_computation_type",
        required=True,
        ondelete="restrict",
        string="Type",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ]
        },
        help="Type of the stock average computation.",
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_product_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Allowed Product Category",
        compute="_compute_allowed_product_category_ids",
        store=False,
        compute_sudo=True,
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Products",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ]
        },
        help="Products to be computed.",
    )
    detail_ids = fields.One2many(
        comodel_name="stock_average_computation.detail",
        inverse_name="stock_average_computation_id",
        string="Details",
        readonly=True,
        help="Details of the stock average computation.",
    )

    # queue
    processing_queue_job_batch_id = fields.Many2one(
        string="Processing Queue Job Batch",
        comodel_name="queue.job.batch",
        readonly=True,
        copy=False,
    )
    processing_queue_job_ids = fields.One2many(
        string="Queue Jobs",
        comodel_name="queue.job",
        related="processing_queue_job_batch_id.job_ids",
        store=False,
    )
    processing_queue_job_batch_state = fields.Selection(
        string="Queue Job Batch State",
        related="processing_queue_job_batch_id.state",
        store=True,
        readonly=True,
    )

    @api.depends("type_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.type_id.product_selection_method,
                    manual_recordset=record.type_id.product_ids,
                    domain=record.type_id.product_domain,
                    python_code=record.type_id.product_python_code,
                )
            record.allowed_product_ids = result

    @api.depends("type_id")
    def _compute_allowed_product_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.category",
                    method_selection=record.type_id.product_category_selection_method,
                    manual_recordset=record.type_id.product_category_ids,
                    domain=record.type_id.product_category_domain,
                    python_code=record.type_id.product_category_python_code,
                )
            record.allowed_product_category_ids = result

    def _default_date(self):
        return date.today()

    def action_queue_processing(self):
        for record in self.sudo():
            record._queue_processing()

    def action_reload_product(self):
        for record in self.sudo():
            record._reload_product()

    def action_reload_detail(self):
        for record in self.sudo():
            record._reload_product()
            record._reload_detail()

    def action_reload_stock_move(self):
        for record in self.sudo():
            record._reload_stock_move()

    def _queue_processing(self):
        self.ensure_one()
        self._reload_product()
        self._reload_detail()
        batch_name = "Stock Average Computation %s" % (self.id or "")
        batch = self.env["queue.job.batch"].get_new_batch(batch_name)
        self.write(
            {
                "processing_queue_job_batch_id": batch.id,
            }
        )
        self._reload_stock_move()

    def _reload_stock_move(self):
        self.ensure_one()
        for detail in self.detail_ids:
            description = (
                "Reload Stock Move for Stock Average Computation Detail %s Header %s"
                % (detail.id, self.id)
            )
            detail.with_context(
                job_batch=self.processing_queue_job_batch_id
            ).with_delay(description=description)._reload_stock_move()
        self.processing_queue_job_batch_id.enqueue()

    def _reload_product(self):
        self.ensure_one()
        criteria = [
            "|",
            ("id", "in", self.allowed_product_ids.ids),
            ("categ_id", "in", self.allowed_product_category_ids.ids),
        ]
        products = self.env["product.product"].search(criteria)
        self.write({"product_ids": [(6, 0, products.ids)]})

    def _reload_detail(self):
        self.ensure_one()
        self._reload_product()
        self.detail_ids.unlink()
        for product in self.product_ids:
            self.env["stock_average_computation.detail"].create(
                {
                    "stock_average_computation_id": self.id,
                    "product_id": product.id,
                    "average_computation_id": product.latest_average_computation_id.id,
                }
            )

    @ssi_decorator.post_done_action()
    def _adjust_svl(self):
        self.ensure_one()
        for detail in self.detail_ids:
            detail._adjust_svl()

    # E.11: insert form elements into view
    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    # E.12: provide additional policy fields
    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
            "reject_ok",
            "manual_number_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res
