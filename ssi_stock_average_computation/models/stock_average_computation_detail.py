# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockAverageComputationDetail(models.Model):
    _name = "stock_average_computation.detail"
    _description = "Stock Average Computation - Detail"
    _order = "product_id, date_cutoff desc"

    stock_average_computation_id = fields.Many2one(
        comodel_name="stock_average_computation",
        string="Stock Average Computation",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        ondelete="restrict",
    )
    average_computation_id = fields.Many2one(
        comodel_name="stock_average_computation.detail",
        string="Average Computation",
        ondelete="set null",
    )
    latest_average_computation_date = fields.Datetime(
        string="Latest Average Computation Date",
        related="average_computation_id.date_cutoff",
        store=True,
        readonly=True,
    )
    date_cutoff = fields.Datetime(
        string="Date Cutoff",
        related="stock_average_computation_id.date_end",
        store=True,
        readonly=True,
    )
    latest_average_cost = fields.Float(
        string="Latest Average Cost",
        related="average_computation_id.average_cost",
        store=True,
        readonly=True,
    )
    latest_quantity = fields.Float(
        string="Latest Quantity",
        related="average_computation_id.qty_total",
        store=True,
        readonly=True,
    )
    latest_value = fields.Float(
        string="Latest Value",
        related="average_computation_id.value_total",
        store=True,
        readonly=True,
    )
    qty_incoming = fields.Float(
        string="Qty Incoming",
        compute="_compute_incoming",
        store=True,
        compute_sudo=True,
    )
    value_incoming = fields.Float(
        string="Value Incoming",
        compute="_compute_incoming",
        store=True,
        compute_sudo=True,
    )
    qty_based = fields.Float(
        string="Qty Based",
        compute="_compute_average_cost",
        store=True,
        compute_sudo=True,
    )
    average_cost = fields.Float(
        string="Average Cost",
        compute="_compute_average_cost",
        store=True,
        compute_sudo=True,
    )
    qty_outgoing = fields.Float(
        string="Qty Outgoing",
        compute="_compute_outgoing",
        store=True,
        compute_sudo=True,
    )
    qty_total = fields.Float(
        string="Qty Total",
        compute="_compute_total",
        store=True,
        compute_sudo=True,
    )
    value_total = fields.Float(
        string="Value Total",
        compute="_compute_total",
        store=True,
        compute_sudo=True,
    )

    stock_move_ids = fields.One2many(
        comodel_name="stock.move",
        inverse_name="stock_average_computation_id",
        string="Stock Moves",
        readonly=True,
    )
    incoming_stock_move_ids = fields.Many2many(
        comodel_name="stock.move",
        string="Incoming Stock Moves",
        compute="_compute_incoming",
        store=False,
        compute_sudo=True,
    )
    outgoing_stock_move_ids = fields.Many2many(
        comodel_name="stock.move",
        string="Outgoing Stock Moves",
        compute="_compute_outgoing",
        store=False,
        compute_sudo=True,
    )
    incoming_transit_stock_move_ids = fields.Many2many(
        comodel_name="stock.move",
        string="Incoming Transit Stock Moves",
        compute="_compute_incoming_transit",
        store=False,
        compute_sudo=True,
    )
    outgoing_transit_stock_move_ids = fields.Many2many(
        comodel_name="stock.move",
        string="Outgoing Transit Stock Moves",
        compute="_compute_outgoing_transit",
        store=False,
        compute_sudo=True,
    )

    svl_to_change_ids = fields.Many2many(
        comodel_name="stock.valuation.layer",
        string="Stock Valuation Layers to Change",
        compute="_compute_svl_to_change",
        store=False,
        compute_sudo=True,
    )

    def _compute_svl_to_change(self):
        for record in self:
            stock_moves = (
                record.outgoing_stock_move_ids
                + record.incoming_transit_stock_move_ids
                + record.outgoing_transit_stock_move_ids
            )
            criteria = [
                ("stock_move_id", "in", stock_moves.ids),
                ("quantity", "!=", 0.0),
            ]
            svl_to_change = self.env["stock.valuation.layer"].search(criteria)
            record.svl_to_change_ids = svl_to_change

    @api.depends("stock_move_ids")
    def _compute_incoming_transit(self):
        for record in self:
            criteria = [
                ("id", "in", record.stock_move_ids.ids),
                ("location_dest_id.usage", "=", "transit"),
                ("location_id.usage", "=", "internal"),
            ]
            stock_moves = self.env["stock.move"].search(criteria)
            record.incoming_transit_stock_move_ids = stock_moves

    @api.depends("stock_move_ids")
    def _compute_outgoing_transit(self):
        for record in self:
            criteria = [
                ("id", "in", record.stock_move_ids.ids),
                ("location_id.usage", "=", "transit"),
                ("location_dest_id.usage", "=", "internal"),
            ]
            stock_moves = self.env["stock.move"].search(criteria)
            record.outgoing_transit_stock_move_ids = stock_moves

    @api.depends("stock_move_ids")
    def _compute_incoming(self):
        for record in self:
            qty = value = 0.0
            criteria = [
                ("id", "in", record.stock_move_ids.ids),
                ("location_dest_id.usage", "=", "internal"),
                ("location_id.usage", "!=", "internal"),
            ]
            stock_moves = self.env["stock.move"].search(criteria)
            record.incoming_stock_move_ids = stock_moves
            for move in stock_moves:
                qty += move.quantity_done
                if move.product_qty != 0:
                    price_unit = (
                        move.product_uom_qty / move.product_qty
                    ) * move.price_unit
                else:
                    price_unit = 0
                value += move.quantity_done * price_unit
            record.qty_incoming = qty
            record.value_incoming = value

    @api.depends("latest_quantity", "qty_incoming", "qty_outgoing", "average_cost")
    def _compute_total(self):
        for record in self:
            record.qty_total = (
                record.latest_quantity + record.qty_incoming - record.qty_outgoing
            )
            record.value_total = record.qty_total * record.average_cost

    @api.depends("stock_move_ids")
    def _compute_outgoing(self):
        for record in self:
            criteria = [
                ("id", "in", record.stock_move_ids.ids),
                ("location_id.usage", "=", "internal"),
                ("location_dest_id.usage", "!=", "internal"),
            ]
            stock_moves = self.env["stock.move"].search(criteria)
            record.outgoing_stock_move_ids = stock_moves
            for move in stock_moves:
                record.qty_outgoing += move.quantity_done

    @api.depends(
        "latest_quantity", "qty_incoming", "latest_average_cost", "value_incoming"
    )
    def _compute_average_cost(self):
        for record in self:
            record.qty_based = record.latest_quantity + record.qty_incoming
            if record.qty_based != 0.0:
                record.average_cost = (
                    record.latest_value + record.value_incoming
                ) / record.qty_based
            else:
                record.average_cost = 0.0

    def _adjust_svl(self):
        self.ensure_one()
        for svl in self.svl_to_change_ids:
            svl.write(
                {
                    "value": self.average_cost * svl.quantity,
                    "unit_cost": self.average_cost,
                }
            )

    def _reload_stock_move(self):
        self.ensure_one()
        criteria = [
            ("state", "=", "done"),
            ("product_id", "=", self.product_id.id),
            ("stock_average_computation_id", "=", False),
            "|",
            "&",
            ("location_id.usage", "!=", "internal"),
            ("location_dest_id.usage", "=", "internal"),
            "&",
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "!=", "internal"),
        ]
        if not self.latest_average_computation_date:
            criteria += [
                ("date", "<=", self.date_cutoff),
            ]
        else:
            criteria += [
                ("date", ">", self.latest_average_computation_date),
                ("date", "<=", self.date_cutoff),
            ]
        stock_moves = self.env["stock.move"].search(criteria)
        stock_moves.write(
            {
                "stock_average_computation_id": self.id,
            }
        )
