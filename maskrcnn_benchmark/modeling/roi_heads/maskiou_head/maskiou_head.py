# Mask Scoring R-CNN
# Wriiten by zhaojin.huang, 2018-12.

import torch
from torch import nn

from maskrcnn_benchmark.structures.boxes import BoxList
from .roi_maskiou_feature_extractors import make_roi_maskiou_feature_extractor
from .roi_maskiou_predictors import make_roi_maskiou_predictor
from .inference import make_roi_maskiou_post_processor
from .loss import make_roi_maskiou_loss_evaluator
from maskrcnn_benchmark.modeling.roi_heads.base_head import ROIBaseHead
from maskrcnn_benchmark.modeling.utils import dfs_freeze


class ROIMaskIoUHead(ROIBaseHead):
    def __init__(self, cfg, in_channels):
        super(ROIMaskIoUHead, self).__init__(cfg=cfg)
        self.use_extended_features = cfg.MODEL.ROI_MASK_HEAD.USE_EXTENDED_FEATURES
        self.feature_extractor = make_roi_maskiou_feature_extractor(cfg)
        self.predictor = make_roi_maskiou_predictor(cfg)
        self.post_processor = make_roi_maskiou_post_processor(cfg)
        self.loss_evaluator = make_roi_maskiou_loss_evaluator(cfg)

    def forward(self, features, proposals, selected_mask=None, labels=None, maskiou_targets=None):
        """
        Arguments:
            features (list[Tensor]): feature-maps from possibly several levels
            proposals (list[BoxList]): proposal boxes
            selected_mask (list[Tensor]): targeted mask
            labels (list[Tensor]): class label of mask
            maskiou_targets (list[Tensor], optional): the ground-truth maskiou targets.

        Returns:
            losses (dict[Tensor]): During training, returns the losses for the
                head. During testing, returns an empty dict.
            results (list[BoxList]): during training, returns None. During testing, the predicted boxlists are returned.
                with the `mask` field set
        """
        if features.shape[0] == 0 and not self.training:
            return {}, proposals

        x = self.feature_extractor(features, selected_mask)
        pred_maskiou = self.predictor(x)

        if not self.training:
            result = self.post_processor(proposals, pred_maskiou, labels)
            return {}, result

        loss_maskiou = self.loss_evaluator(labels, pred_maskiou, maskiou_targets)

        return dict(loss_maskiou=loss_maskiou), None


def build_roi_maskiou_head(cfg):
    model = ROIMaskIoUHead(cfg)

    if cfg.MODEL.ROI_MASK_HEAD.FREEZE:
        dfs_freeze(model, requires_grad=False)
    return model

