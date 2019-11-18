# -*- coding: utf-8 -*-
# ©2018-2019 Article714
# # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    informa_visibility = fields.Boolean(
        compute="_compute_informa_visibility", default=False
    )

    informa_use_parent_company = fields.Boolean(default=False)

    informa_url = fields.Char()
    informa_username = fields.Char()
    informa_password = fields.Char()

    informa_parent_url = fields.Char(compute="_compute_parent_url")
    informa_parent_username = fields.Char(compute="_compute_parent_username")
    informa_parent_password = fields.Char(compute="_compute_parent_password")

    @api.depends("parent_id")
    @api.onchange("parent_id", "informa_use_parent_company")
    def _compute_parent_url(self):
        for rec in self:
            if rec.parent_id and rec.informa_use_parent_company:
                rec.informa_parent_url = rec.get_parent_field("informa_url")

    @api.depends("parent_id")
    @api.onchange("parent_id", "informa_use_parent_company")
    def _compute_parent_username(self):
        for rec in self:
            if rec.parent_id and rec.informa_use_parent_company:
                rec.informa_parent_username = rec.get_parent_field(
                    "informa_username"
                )

    @api.depends("parent_id")
    @api.onchange("parent_id", "informa_use_parent_company")
    def _compute_parent_password(self):
        for rec in self:
            if rec.parent_id and rec.informa_use_parent_company:
                rec.informa_parent_password = rec.get_parent_field(
                    "informa_password"
                )

    @api.depends("coreff_connector_id")
    @api.onchange("coreff_connector_id")
    def _compute_informa_visibility(self):
        for rec in self:
            if rec.coreff_connector_id == self.env.ref(
                "coreff_informa.coreff_connector_informa_api"
            ):
                rec.informa_visibility = True
            else:
                rec.informa_visibility = False

    def get_parent_field(self, field):
        for rec in self:
            if not rec.informa_use_parent_company:
                return rec[field]
            elif rec.parent_id:
                return rec.parent_id.get_parent_field(field)
            else:
                return None
