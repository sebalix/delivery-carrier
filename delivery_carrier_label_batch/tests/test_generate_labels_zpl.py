# -*- coding: utf-8 -*-
# Copyright 2013-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp.modules import get_module_resource

from .common import CommonGenerateLabels


class TestGenerateLabelsZPL(CommonGenerateLabels):
    """Test the wizard for delivery carrier label generation (ZPL)."""

    @classmethod
    def setUpClass(cls):
        super(TestGenerateLabelsZPL, cls).setUpClass()

        label = ''
        dummy_zpl_path = get_module_resource(
            'delivery_carrier_label_batch', 'tests', 'dummy.zpl2')
        with file(dummy_zpl_path) as dummy_zpl:
            label = dummy_zpl.read()

        ShippingLabel = cls.env['shipping.label']
        ShippingLabel._fields['file_type'].selection = (
            lambda obj: [('pdf', 'PDF'), ('zpl2', 'ZPL2')])
        ShippingLabel.create(
            {'name': 'picking_out_1',
             'res_id': cls.picking_out_1.id,
             'res_model': 'stock.picking',
             'datas': label.encode('base64'),
             'file_type': 'zpl2',
             })

        ShippingLabel.create(
            {'name': 'picking_out_2',
             'res_id': cls.picking_out_2.id,
             'res_model': 'stock.picking',
             'datas': label.encode('base64'),
             'file_type': 'zpl2',
             })

    def test_00_action_generate_labels(self):
        """ Check merging of ZPL labels

        We don't test ZPL generation as without dependancies the
        test would fail

        """
        wizard = self.env['delivery.carrier.label.generate'].with_context(
            active_ids=self.batch.ids,
            active_model='stock.batch.picking').create({})
        wizard.action_generate_labels()

        attachment = self.env['ir.attachment'].search(
            [('res_model', '=', 'stock.batch.picking'),
             ('res_id', '=', self.batch.id)]
        )

        self.assertEquals(len(attachment), 1)
        self.assertTrue(attachment.datas)
        self.assertTrue(attachment.name, 'demo_prep001.zpl2')
        self.assertTrue(attachment.mimetype, 'application/pdf')
