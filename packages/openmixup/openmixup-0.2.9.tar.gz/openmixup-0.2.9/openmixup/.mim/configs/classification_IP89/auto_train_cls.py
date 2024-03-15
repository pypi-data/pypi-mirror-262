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
                    cmd = 'CUDA_VISIBLE_DEVICES=0 PORT={} bash tools/dist_train.sh {} {} &\nsleep 1s \n'.format(port, file_name, self.num_device)
                    shfile.write(cmd)
                shfile.write('\n')
    print('Generation completed.')


def main():
    # base_path = 'configs/classification/stl10/automixV2/v0823/r18_layer2_cosh_addi_cos_loss_01_FFN_conv3x3_eg_drop_01.py'
    # base_path = 'configs/classification/stl10/automixV2/v0823/r18_layer2_cosh_addi_cos_loss_01_FFN_conv3x3_eg.py'
    # 08.24
    base_path = "configs/classification/stl10/automixV2/v0824/r18_v0824_L2_cosh_addi_cos_loss_01_lr_min5e_2_FFN_conv3x3_eg_drop01.py"

    # emix
    abbs = {
        'total_epochs': 'ep'
    }
    # create nested dirs
    model_var = {
        'model.mix_block.lam_mul': [True,],
        'model.mix_block.x_qk_concat': [True,],  # ok
        'model.alpha': [2,],  # STL,
    }
    gm_var = {
        # 'model.alpha': [2,],  # ok
        # 'model.mix_block.unsampling_mode': ['nearest', 'bilinear'],  # try
        'model.mix_block.unsampling_mode': ['bilinear'],  # STL, OK
        # 'model.mix_block.mask_loss_mode': ['L2+Variance', 'L1+Variance',],  # v08.24
        # 'model.mix_block.loss_mode': ['L2+Variance', 'L1+Variance',],  # ori
        # 'model.mix_block.loss_mode': ['L1+Variance',],  # ok
        'model.mix_block.mask_loss_mode': ['L2+Variance',],  # v08.24
        # 'model.pre_one_loss': [1, 0.1, 0.5],  # try
        'model.pre_one_loss': [1, 0.1,],  # try
        # 'model.pre_mix_loss': [1, 0.1, 0.5],  # try
        'model.pre_mix_loss': [1, 0.1,],  # try
        # 'model.mix_block.x_qk_concat': [True, False],  # try
        # 'optimizer.paramwise_options.mix_block.momentum': [0, 0.9],  # STL, try
        # 'addtional_scheduler.min_lr': [0,],  # STL cosine, ok
        'addtional_scheduler.min_lr': [0.05],  # STL cosine, try
        'lr_config.min_lr': [0.05],  # STL
        'total_epochs': [400, ]
    }
    
    num_device = 1
    
    generator = ConfigGenerator(base_path=base_path, num_device=num_device)
    generator.generate(model_var, gm_var, abbs)


if __name__ == '__main__':
    main()