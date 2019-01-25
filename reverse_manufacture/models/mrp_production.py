# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
import math

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    @api.multi
    def button_mark_done(self):
        if not self.state == 'progress':
            # Nothing to do for lots since values are created using default data (stock.move.lots)
            moves = self.move_raw_ids
            quantity = self.product_qty
            #check finished products
            lots = self.env['stock.move.lots']
            produce_move = self.move_finished_ids.filtered(lambda x: x.product_id == self.product_id and x.state not in ('done', 'cancel'))
            if produce_move and produce_move.product_id.tracking != 'none':
                lot_id = produce_move.move_lot_ids and produce_move.move_lot_ids[0].lot_id
                existing_move_lot = produce_move.move_lot_ids and produce_move.move_lot_ids[0]

                vals = {
                  'move_id': produce_move.id,
                  'product_id': produce_move.product_id.id,
                  'production_id': self.id,
                  'quantity': self.product_qty,
                  'quantity_done': self.product_qty,
                  'lot_id': lot_id.id,
                }
                existing_move_lot.write(vals)

                for move in self.move_raw_ids:
                    for movelots in move.move_lot_ids.filtered(lambda x: not x.lot_produced_id):
                        if movelots.quantity_done and lot_id:
                            #Possibly the entire move is selected
                            remaining_qty = movelots.quantity - movelots.quantity_done
                            if remaining_qty > 0:
                                default = {'quantity': movelots.quantity_done, 'lot_produced_id': lot_id.id}
                                new_move_lot = movelots.copy(default=default)
                                movelots.write({'quantity': remaining_qty, 'quantity_done': 0})
                            else:
                                movelots.write({'lot_produced_id': lot_id.id})
            
            

        return super(MrpProduction, self).button_mark_done()