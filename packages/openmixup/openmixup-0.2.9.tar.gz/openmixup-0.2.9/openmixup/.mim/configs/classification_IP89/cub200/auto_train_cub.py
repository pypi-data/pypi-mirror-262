import json
import os
import argparse

from datetime import datetime
from mmcv import Config
# from numpy.core.fromnumeric import prod, var
# from tools.train import main
# from openselfsup.apis import train
from functools import reduce
from operator import getitem
from itertools import product


class ConfigGenerator:
    def __init__(self, base_path: str, num_device: int) -> None:
        self.base_path = base_path
        self.num_device = num_device

    def _path_parser(self, path: str) -> str:
        assert isinstance(path, str)
        base_dir = os.path.join(*self.base_path.split('/')[:-1])
        base_name = self.base_path.split('/')[-1] # file name
        base_prefix = base_name.split('.')[0] # prefix
        backbone = base_prefix.split('_')[0]

        return base_dir, backbone, base_prefix

    def _combinations(self, var_dict: dict) -> list:
        assert isinstance(var_dict, dict)
        ls = list(var_dict.values())
        cbs = [x for x in product(*ls)] # all combiantions

        return cbs

    def set_nested_item(self, dataDict: dict, mapList: list, val) -> dict:
        """Set item in nested dictionary"""
        reduce(getitem, mapList[:-1], dataDict)[mapList[-1]] = val

        return dataDict

    def generate(self, model_var: dict, gm_var: dict, abbs: dict) -> None:
        assert isinstance(model_var, dict)
        assert isinstance(gm_var, dict)
        cfg = dict(Config.fromfile(self.base_path))
        base_dir, backbone, base_prefix = self._path_parser(self.base_path) # analysis path
        model_cbs = self._combinations(model_var)
        gm_cbs = self._combinations(gm_var)

        # params for global .sh file
        port = 99999
        time = datetime.today().strftime('%Y%m%d_%H%M%S')
        with open('{}_{}.sh'.format(os.path.join(base_dir, base_prefix), time), 'a') as shfile:
            # model setting
            for c in model_cbs:
                cfg_n = cfg # reset
                config_dir = os.path.join(base_dir, backbone)
                for i, kv in enumerate(zip(list(model_var.keys()), c)):
                    k = kv[0].split('.')
                    v = kv[1]
                    cfg_n = self.set_nested_item(cfg_n, k, v) # assign value
                    config_dir += '/{}{}'.format(str(k[-1]), str(v))
                comment = ' '.join(config_dir.split('/')[-i-1:]) # e.g. alpha1.0 mask_layer 1
                shfile.write('# {}\n'.format(comment))

                # base setting
                for b in gm_cbs:
                    base_params = ''
                    for kv in zip(list(gm_var.keys()), b):
                        a = kv[0].split('.')
                        n = kv[1]
                        cfg_n = self.set_nested_item(cfg_n, a, n)
                        base_params += '_{}{}'.format(str(a[-1]), str(n))

                    # saving json config
                    config_dir = config_dir.replace('.', '_')
                    base_params = base_params.replace('.', '_')
                    for word, abb in abbs.items():
                        base_params = base_params.replace(word, abb)
                    if not os.path.exists(config_dir):
                        os.makedirs(config_dir)
                    file_name = os.path.join(config_dir, '{}{}.json'.format(base_prefix, base_params))
                    with open(file_name, 'w') as configfile:
                        json.dump(cfg, configfile, indent=4)

                    # write cmds for .sh
                    port += 1
                    cmd = 'CUDA_VISIBLE_DEVICES=0 PORT={} bash tools/dist_train.sh {} {} &\nsleep 0.01s \n'.format(port, file_name, self.num_device)
                    shfile.write(cmd)
                shfile.write('\n')
    print('Generation completed.')


def main():
    # 12.09, decouple
    # base_path = "configs/classification/cub200/automix/v0824_1209/r18_v0824_l2_1209_lam_cat_CE_use_soft_mlr5e_4.py"
    # base_path = "configs/classification/cub200/automix/v0824_1209/rx50_v0824_l2_1209_lam_cat_CE_use_soft_mlr5e_4.py"
    # base_path = "configs/classification/cub200/automix/v0824_1209/rx50_v0824_l2_1209_lam_cat_CE_use_soft_mlr5e_4_m0.py"
    base_path = "configs/classification_IP89/cub200/mixup/rx50_mixup_1209_CE_use_soft.py"

    # 12.19, try pretrained_k
    # iNat
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r18_iNat.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r50_iNat.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_rx101_iNat.py"
    # CUB
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r18_cub.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_rx50_cub.py"
    # IN
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r18_IN.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r18_IN_300e.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r50_IN.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r50_IN_mix_only.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r50_IN_300e.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r101_IN.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/r18_v0824_1219_dp01_val_pretrain_k_r101_IN_300e.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/rx50_v0824_1219_dp01_val_pretrain_k_r18_IN.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/rx50_v0824_1219_dp01_val_pretrain_k_r50_IN.py"
    # base_path = "configs/classification/cub200/automixV2/pretrained_k/rx50_v0824_1219_dp01_val_pretrain_k_r101_IN.py"

    # 01.10
    # base_path = "configs/classification/cub200/automixV2/v0824_0109/r18_v0824_l2_dp01_val_CE_use_soft_mlr5e_4.py"
    # 01.18
    # base_path = "configs/classification/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_cut1_p033_resize1_p033_manifold02_p033.py"
    # base_path = "configs/classification/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_mix01_p033_cut1_p033_manifold05_p033.py"
    # base_path = "configs/classification/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_mix01_p033_cut2_p033_manifold05_p033.py"
    # base_path = "configs/classification/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_mix01_p033_resize1_p033_manifold05_p033.py"
    # base_path = "configs/classification/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_cut1_p033_resize1_p033_manifold02_p033_repeat2.py"
    # base_path = "configs/classification/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_mix01_p033_cut1_p033_manifold05_p033_repeat2.py"
    # base_path = "configs/classification_IP89/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_cut2_p033_resize1_p033_manifold01_p033_repeat2.py"
    # base_path = "configs/classification_IP89/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_cut1_p033_resize1_p033_mix01_p033_repeat2.py"
    # base_path = "configs/classification_IP89/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_cut2_p033_resize1_p033_mix01_p033_repeat2.py"
    # base_path = "configs/classification_IP89/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_cut1_p033_resize1_p033_mix01_p033.py"
    # base_path = "configs/classification_IP89/cub200/baseline/no_randaug_mix_mode3/r50_cls_448_cut2_p033_resize1_p033_mix01_p033.py"
    #
    # base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50/mask_input_size_11_10_09_08/r50_v0824_l2_0128_dp01_val_CE_sz448_mb_up1.py"
    # base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50/mask_input_size_12_10_08_06/r50_v0824_l2_0128_dp01_val_CE_sz448_mb_up1.py"
    # base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50/mask_input_size_12_11_10_09_08_07/r50_v0824_l2_0128_dp01_val_CE_sz448_mb_up1.py"
    # base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50/mask_input_size_13_12_11_10/r50_v0824_l2_0128_dp01_val_CE_sz448_mb_up1.py"
    # base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50/mask_input_size_14_12_10_08/r50_v0824_l2_0128_dp01_val_CE_sz448_mb_up1.py"
    # base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50/mask_input_size_14_13_12_11/r50_v0824_l2_0128_dp01_val_CE_sz448_mb_up1.py"
    # base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50/mask_input_size_13_12_11_10/r50_v0824_l3_0128_dp01_val_CE_sz448_mb_up1.py"

    # emix
    abbs = {
        'total_epochs': 'ep'
    }
    # create nested dirs
    model_var = {
        # 01.09
        # 'model.mix_repeat': [1,],
        # 12.09, decouple
        'model.head.loss.use_mix_decouple': [True,],  # mixup decouple
        # 'model.head_mix.loss.use_mix_decouple': [True,],  # AutoMix decouple
        # 'model.head_mix.loss.use_mix_decouple': [False,],  # AutoMix decouple F
        # 12.19
        # 'model.momentum': [1,],  # try pretrained mixblock
        # 'model.mix_block.unsampling_mode': ['bilinear', 'nearest',],
        # 'model.mix_block.unsampling_mode': ['bilinear',],
        # 'model.mask_up_override': ['bilinear',],
        'model.mix_mode': ['mixup', 'cutmix', 'fmix', 'saliencymix', 'resizemix', 'manifoldmix',],
    }
    gm_var = {
        # 'model.alpha': [2, 4,],
        # 'model.alpha': [0.1, 0.2, 0.5, 1,],
        # 'model.alpha': [0.5, 1, 2, 4, ],
        'model.alpha': [0.2, ],
        # 'model.mix_block.lam_mul_k': [0, 0.25, 0.5, 1],
        # 'model.mix_block.lam_mul_k': [0.25, 1],
        # 'model.mask_adjust': [0, 0.25, ],
        # 'model.mask_adjust': [0.25, ],
        # 'model.mix_block.unsampling_mode': ['nearest',],
        # 'model.mix_block.unsampling_mode': ['bilinear', 'nearest',],
        # 'model.mask_up_override': ['bilinear', 'nearest',],
        #
        ### lam decouple
        # 'model.head.two_hot_thr': [0.7, 0.8, 0.9],
        # 'model.head.two_hot_idx': [0.3, 0.5, 1, 2, 3],
        'model.head.lam_idx': [0, 1],  # mixup baseline, try lam idx
        # 'model.head.lam_idx': [1,],  # mixup baseline, lam idx, OK
        # 'model.head.eta_weight.eta': [0.1, ],  # mixup baseline, eta, OK
        'model.head.eta_weight.eta': [1, 0.5, 0.1, 0.01],  # mixup baseline, try eta
        # 'model.head.eta_weight.mode': ["both"],  # mixup baseline, eta biased, OK
        'model.head.eta_weight.mode': ["less"],  # mixup baseline, eta biased, try
        #
        ##### 12.09, decouple (automix) ####
        # # 'model.head_mix.lam_idx': [0, 1,],  # AutoMix, try lam idx
        # 'model.head_mix.lam_idx': [0, 0.5, ],  # AutoMix, OK lam idx
        # # 'model.head_mix.eta_weight.eta': [1, 0.5, 0.1, 0.01,],  # AutoMix, try eta
        # 'model.head_mix.eta_weight.eta': [1, 0.5, 0.1, 0.01,],  # AutoMix, OK eta
        # # 'model.head_mix.eta_weight.mode': ["both", "more", "less"],  # AutoMix, try eta biased
        # 'model.head_mix.eta_weight.mode': ["both", ],  # AutoMix, ok eta biased
        # # 'model.head_mix.eta_weight.thr': [0.5,],  # AutoMix, eta biased
        #
        # 'optimizer.paramwise_options.mix_block.lr': [1e-2, ],  # AutoMix, ok
        # 'optimizer.lr': [1e-3, 2e-3,],  # mixup lr, try
        # 'optimizer.lr': [2e-3,],  # mixup lr, ok
        # 'optimizer.paramwise_options.head.lr': [2e-2, 5e-2,],  # mixup head, try
        # 'addtional_scheduler.min_lr': [5e-3, 5e-4,],  # AutoMix, try
        # semi
        # 'total_epochs': [130,]  # per 15
        'total_epochs': [200,]  # per 50
        # 'total_epochs': [400,]
        # 'total_epochs': [100,]
    }
    
    num_device = 1
    
    generator = ConfigGenerator(base_path=base_path, num_device=num_device)
    generator.generate(model_var, gm_var, abbs)


if __name__ == '__main__':
    main()