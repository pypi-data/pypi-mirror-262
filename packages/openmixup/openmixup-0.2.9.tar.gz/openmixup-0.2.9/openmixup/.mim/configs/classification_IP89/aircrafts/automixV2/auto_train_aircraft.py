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
    # 11.22
    # base_path = "configs/classification/aircrafts/mixups/r18_mixups_1122_CE_use_soft.py"
    
    # 12.09
    # base_path = "configs/classification/aircrafts/mixups/r18_mixup_1209_CE_use_soft.py"
    # base_path = "configs/classification/aircrafts/mixups/rx50_mixup_1209_CE_use_soft.py"
    
    # 01.09, 448
    base_path = "configs/classification/aircrafts/automixV2/v0824_0109/r50_v0824_l3_0109_dp01_val_CE_use_soft_sz448_mb_up0.py"

    # emix
    abbs = {
        'total_epochs': 'ep'
    }
    # create nested dirs
    model_var = {
        # 'model.alpha': [2,],
        # 'model.head.loss.use_mix': [True],  # use_mix for mix baselines
        # 'model.head.loss.use_mix_decouple': [True,],  # mixup baseline
        'model.head_mix.loss.use_mix_decouple': [False,],  # AutoMix decouple F
        # 'model.head_mix.loss.use_mix_decouple': [True,],  # AutoMix decouple
    }
    gm_var = {
        # 'model.alpha': [2,],
        # 'model.alpha': [0.1, 0.2, 0.5, 1,],
        # 'model.alpha': [0.2, ],
        # 'model.alpha': [0.2, ],
        # 'model.mix_block.lam_mul_k': [0, 0.25, 0.5, 1],
        # 'model.mix_block.lam_mul_k': [0.25, 1],
        # 'model.head.two_hot_mode': ['pow'],
        # 'model.head.two_hot_thr': [1],
        # # 'model.head.loss.use_eta': [1, 0.5, 0.1, 0.01],  # try use_eta for mix baselines
        # 'model.head.loss.use_eta': [5, 2],  # try use_eta for mixup
        #
        # ##### 12.09, decouple (mixup) ####
        # # 'model.head.lam_idx': [0, 0.5, 1,],  # mixup, try lam idx
        # 'model.head.lam_idx': [0, 1,],  # mixup, try lam idx
        # 'model.head.eta_weight.eta': [1, 0.5, 0.1, 0.01,],  # mixup, try eta
        # # 'model.head.eta_weight.eta': [0.5,],  # mixup, ok eta
        # # 'model.head.eta_weight.mode': ["both", "more", "less"],  # mixup, try eta biased
        # 'model.head.eta_weight.mode': ["less", ],  # mixup, ok eta biased
        # 'model.head.eta_weight.thr': [0.5,],  # mixup, eta biased
        #
        # ### 448, AutoMix
        'optimizer.lr': [1e-3, 2e-3, 5e-3],  # lr, try
        # 'optimizer.paramwise_options.head.lr': [1e-2, 5e-2,],  # head, try
        'optimizer.paramwise_options.head.lr': [1e-2, ],  # head, ok
        # 'optimizer.paramwise_options.mix_block.lr': [1e-2, 5e-2,],  # AutoMix, try
        'optimizer.paramwise_options.mix_block.lr': [1e-2, ],  # AutoMix, ok
        # 'addtional_scheduler.min_lr': [1e-2, 1e-3, ],  # AutoMix, try
        'addtional_scheduler.min_lr': [1e-3, 5e-4,],  # AutoMix, ok
        #
        'total_epochs': [100,]
        # 'total_epochs': [200,]
        # 'total_epochs': [400,]
        # 'total_epochs': [800,]
    }
    
    num_device = 1
    
    generator = ConfigGenerator(base_path=base_path, num_device=num_device)
    generator.generate(model_var, gm_var, abbs)


if __name__ == '__main__':
    main()