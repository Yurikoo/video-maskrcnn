# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

from maskrcnn_benchmark.utils.registry import Registry

BACKBONES = Registry()
RPN_HEADS = Registry()

ROI_BOX_FEATURE_EXTRACTORS = Registry()
ROI_BOX_PREDICTOR = Registry()
ROI_KEYPOINT_FEATURE_EXTRACTORS = Registry()
ROI_KEYPOINT_PREDICTOR = Registry()
ROI_MASK_FEATURE_EXTRACTORS = Registry()
ROI_MASK_PREDICTOR = Registry()

ROI_PRED_FEATURE_EXTRACTORS = Registry()
ROI_PRED_PREDICTOR = Registry()

DECODER_CLS_FEATURE_EXTRACTORS = Registry()
DECODER_CLS_PREDICTOR = Registry()

ATTENTION_MECHANISM = Registry()

POOLER = Registry()
