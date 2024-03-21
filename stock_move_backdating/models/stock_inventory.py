#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from ..utils import check_date


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    date_backdating = fields.Datetime(
        string="Actual Inventory Date",
    )

    @api.onchange(
        "date_backdating",
    )
    def onchange_date_backdating(self):
        self.ensure_one()
        check_date(self.date_backdating)

    def post_inventory(self):
        no_backdate_inventories = self.env["stock.inventory"]
        for inventory in self:
            date_backdating = inventory.date_backdating
            if date_backdating:
                inventory_ctx = inventory.with_context(
                    date_backdating=date_backdating,
                )
                super(StockInventory, inventory_ctx).post_inventory()
            else:
                no_backdate_inventories |= inventory
        res = super(StockInventory, no_backdate_inventories).post_inventory()
        moves = self.mapped("move_ids")
        moves._backdating_account_moves()
        moves._backdating_stock_valuation_layers()
        return res
