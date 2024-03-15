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

    # 11.10
    # base_path = "configs/classification/cifar100/automixV2/v0824_1110/r18_v0824_1110_l2_dp0_CE_use_soft_CE_q_BCE_k_pow_neg.py"
    # base_path = "configs/classification/cifar100/automixV2/v0824_1110/rx50_v0824_1110_l2_dp0_CE_use_soft_CE_q_BCE_k_pow_neg.py"
    # 11.22
    # base_path = "configs/classification/cifar100/mixup/r18_mixups_v1122_CE_use_soft.py"
    # base_path = "configs/classification/cifar100/automixV2/v0824_1110/r18_v0824_1122_l2_dp0_CE_use_soft_use_mix.py"
    # 11.28
    # base_path = "configs/classification/cifar100/mixup/r18_mixups_v1128_CE_use_soft.py"
    # base_path = 'configs/classification/cifar100/automixV2/v0824_1110/r18_v0824_1128_l2_dp0_CE_use_soft_use_mix.py'
    # base_path = "configs/classification/cifar100/automixV2/v0824_1110/r18_v0824_1128_l2_dp0_CE_use_soft_use_mix_m0.py"
    # 01.09
    # base_path = "configs/classification/cifar100/automixV2/v0824_0109/r18_v0824_l2_dp0_val_smooth_mb_up.py"
    # base_path = "configs/classification/cifar100/automixV2/v0824_0109/r18_v0824_l2_dp0_val_smooth_mb_CE_up.py"
    # base_path = "configs/classification/cifar100/automixV2/v0824_0109/r18_v0824_l2_dp0_val_smooth_decoup_mb_up.py"
    base_path = "configs/classification/cifar100/automixV2/v0824_0109/r18_v0824_l2_dp0_val_smooth_decoup_mb_CE_up.py"

    abbs = {
        'total_epochs': 'ep'
    }
    # create nested dirs
    model_var = {
        # 'model.mix_mode': ['mixup', 'cutmix', 'fmix',],
        # 'model.head.loss.use_mix': [True],  # use_mix for mix baselines
        # 'model.head_mix.loss.use_mix': [True],  # use_mix AutoMix
        'model.head_mix.loss.mode': ['mix_decouple'],  # AutoMix, try decouple
        # 'model.head_mix.loss.mode': ['original'],  # AutoMix, label smooth
        # 'model.head.two_hot': [True],
        # 'model.head_mix.two_hot': [False],
        # 'model.head_mix.two_hot': [True],
        # 'model.head_mix.two_hot_mode': ['pow'],
        # 'model.head_mix_k.two_hot_mode': ['pow'],
        # 'model.head_mix_k.two_hot': [False],
        # 'model.head_mix_k.two_hot': [True],
        # 'model.mix_block.unsampling_mode': ['bilinear',],
    }
    gm_var = {
        # 'model.alpha': [2, 4],
        # 'model.alpha': [2,],
        # 'model.alpha': [0.1, 0.2, 0.5, 1,],
        # 'model.alpha': [0.2, 1,],
        # 'model.mix_block.lam_mul_k': [0, 0.25, 0.5, 1],
        # 'model.mix_block.lam_mul_k': [0.25, 1],
        'model.mix_block.lam_mul_k': [0, 1],
        # 'model.head.two_hot_mode': ['pow'],
        # 'model.head.two_hot_mode': ['none', 'pow'],
        # 'model.head_mix.two_hot_mode': ['pow'],
        # 'model.head_mix_k.two_hot_mode': ['pow'],
        # 'model.head_mix_k.two_hot_scale': [0.25, 0.5, 1,],
        # 'model.head_mix.two_hot_scale': [0.5, 1,],
        # 'model.head_mix.two_hot_thr': [0.7, 0.8, 0.9],
        # 'model.head_mix.two_hot_thr': [1],
        # 'model.head.two_hot_thr': [0.8, 1],
        # 'model.head.two_hot_thr': [1],
        # 'model.head_mix.loss.use_lam': [False, True],  # try use_lam, AutoMix
        # 'model.head_mix.loss.use_lam': [True],  # try use_lam, AutoMix, OK
        # 'model.head.loss.use_eta': [1, 0.5, 0.1, 0.01],  # try use_eta for mix baselines
        # 'model.head_mix.loss.use_eta': [1, 0.5, 0.1, 0.01],  # try use_eta for AutoMix
        # 'model.head_mix.loss.use_eta': [0.01, 0.5],  # try use_eta for AutoMix
        # 'model.head_mix.loss.use_eta': [1, 2, 4, 10],  # try use_eta for AutoMix
        # 'model.head_mix.loss.use_eta': [0.01, 0.5, 1, 2],  # try use_eta for AutoMix
        # 'model.head_mix.loss.use_eta': [0.5, 1,],  # AutoMix
        # 'model.head_mix.loss.use_eta': [1, 2],  # AutoMix
        # 'model.head_mix.loss.use_eta': [1,],  # AutoMix OK
        # 'model.head_mix.loss.use_idx': [0.3, 0.5,],  # try use_idx when use_lam, AutoMix
        # 'model.head_mix.two_hot_thr': [1],
        # 'model.head_mix_k.two_hot_thr': [0.6, 0.8, 1],
        # 'model.head_mix.two_hot_thr': [0.6, 0.8, 1],
        # 'model.head_mix.two_hot_idx': [0.3, 0.5, 1, 2, 3],
        # 'model.head_mix.two_hot_idx': [0.5, 1,],
        # 'model.head_mix_k.two_hot_idx': [0.5, 1,],
        # automix decouple
        # 'model.head_mix.lam_idx': [0, 0.5, ],  # AutoMix, try lam idx
        'model.head_mix.lam_idx': [0.5,],  # AutoMix, lam idx
        'model.head_mix.eta_weight.eta': [1, 0.5, 0.1, 0.01,],  # AutoMix, try eta
        # 'model.head_mix.eta_weight.eta': [0.1, 0.01,],  # AutoMix, ok eta
        # 'model.head_mix.eta_weight.mode': ["both", "more", "less"],  # AutoMix, try eta biased
        'model.head_mix.eta_weight.mode': ["both", ],  # AutoMix, ok eta biased
        # 'model.head_mix.eta_weight.mode': ["less",],  # AutoMix, ok eta biased
        'model.head_mix.eta_weight.thr': [0.5,],  # AutoMix, eta biased
        #
        # 'model.head_mix_k.neg_weight': [0, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1],
        # 'model.head_mix_k.neg_weight': [0.01, 0.1, 0.5, 1],  # AutoMix
        # 'model.head_mix_k.neg_weight': [0.01, 0.5,],  # AutoMix
        # 'model.head_mix_k.neg_weight': [0.5,],  # AutoMix, OK
        # 'model.head_mix_k.neg_weight': [1,],  # AutoMix.V2, OK
        'model.mask_adjust': [0, 0.25],
        # 'model.mask_adjust': [0,],
        # 'model.mask_adjust': [0.25,],
        # 'model.mix_block.lam_mul_k': [0.25, 0.5,],
        # 'model.mix_block.lam_mul_k': [0.5,],
        # 'model.mix_block.lam_concat_v': [False,],
        # 'model.mix_block.mask_loss_mode': ["L1+Variance", "Variance"],
        # 'model.mix_block.mask_loss_mode': ["L1+Variance", ],
        'total_epochs': [400,]
        # 'total_epochs': [800,]
    }
    
    num_device = 1
    
    generator = ConfigGenerator(base_path=base_path, num_device=num_device)
    generator.generate(model_var, gm_var, abbs)


if __name__ == '__main__':
    main()