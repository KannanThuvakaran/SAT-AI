import torch
import torch.nn as nn
import numpy as np
from ever.interface import ERModule
from ever import registry
from module.seg_base import AssymetricDecoder, FPN, default_conv_block
from segmentation_models_pytorch.encoders import get_encoder

def check_targets(cls_true, n_classes):
    min_val = torch.min(cls_true)
    max_val = torch.max(cls_true)
    if min_val < 0 or max_val >= n_classes:
        raise ValueError(f"Target values out of range: min={min_val}, max={max_val}")

@registry.MODEL.register('SemanticFPN')
class SemanticFPN(ERModule):
    def __init__(self, config):
        super(SemanticFPN, self).__init__(config)
        self.en = get_encoder(**self.config.encoder)
        self.fpn = FPN(**self.config.fpn)
        self.decoder = AssymetricDecoder(**self.config.decoder)
        self.cls_pred_conv = nn.Conv2d(self.config.decoder.out_channels, self.config.classes, 1)
        self.upsample4x_op = nn.UpsamplingBilinear2d(scale_factor=4)
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.ce_loss = nn.CrossEntropyLoss(ignore_index=self.config.loss.ignore_index)

    def forward(self, x, y=None):
        feat_list = self.en(x)
        if len(feat_list) == 5:
            feat_list = feat_list[1:]
        fpn_feat_list = self.fpn(feat_list)
        final_feat = self.decoder(fpn_feat_list)
        cls_pred = self.cls_pred_conv(final_feat)
        cls_pred = self.upsample4x_op(cls_pred)
        
        if self.training:
            cls_true = y['mask'].long().to(self.device)
            cls_true = (cls_true / 255).long()
            check_targets(cls_true, self.config.classes)

            assert cls_pred.shape[1] == self.config.classes
            assert cls_pred.shape[2:] == cls_true.shape[1:]

            loss_dict = dict()
            loss_dict['seg_loss'] = self.ce_loss(cls_pred, cls_true)
            mem = torch.cuda.max_memory_allocated() // 1024 // 1024
            loss_dict['mem'] = torch.tensor([mem], dtype=torch.float32).to(self.device)
            return loss_dict
        else:
            return cls_pred.softmax(dim=1), feat_list[-1]


    def set_default_config(self):
        self.config.update(dict(
            encoder=dict(
                name='resnet50',
                weights='imagenet',
                in_channels=3
            ),
            fpn=dict(
                in_channels_list=(256, 512, 1024, 2048),
                out_channels=256,  # Reduced output channels
                conv_block=default_conv_block,
                top_blocks=None,
            ),
            decoder=dict(
                in_channels=256,  # Matching reduced FPN output channels
                out_channels=128,  # Adjusted to fit new FPN output
                in_feat_output_strides=(4, 8, 16, 32),
                out_feat_output_stride=4,
                norm_fn=nn.BatchNorm2d,
                num_groups_gn=None
            ),
            classes=2,
            loss=dict(
                ignore_index=-1, # was -1
            )
        ))




