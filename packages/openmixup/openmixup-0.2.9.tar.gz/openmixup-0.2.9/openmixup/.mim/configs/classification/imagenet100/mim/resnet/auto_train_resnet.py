from openmixup.utils import ConfigGenerator


def main():
    """Automatic Config Generator: generate openmixup configs in terms of keys"""

    base_path = ""

    # abbreviation of long attributes
    abbs = {
        'total_epochs': 'ep'
    }
    # create nested dirs (cannot be none)
    model_var = {
        'model.backbone.mask_token': ['learnable', 'mean',],
    }
    # adjust sub-attributes (cannot be none)
    gm_var = {
        # 'model.neck_cls.use_mask': [True, False,],
        'model.neck_cls.use_mask': [False,],
        'model.head_mim.unmask_weight': [0, 0.1,],
        'total_epochs': [400,],
    }
    
    num_device = 1
    
    generator = ConfigGenerator(base_path=base_path, num_device=num_device)
    generator.generate(model_var, gm_var, abbs)


if __name__ == '__main__':
    main()