# Copyright 2018 Alex Comba - Agile Business Group
# Copyright 2023 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields
from odoo.exceptions import UserError


def check_date(date):
    now = fields.Datetime.now()
    if date and date > now:
        raise UserError(_("You can not process an actual movement date in the future."))
