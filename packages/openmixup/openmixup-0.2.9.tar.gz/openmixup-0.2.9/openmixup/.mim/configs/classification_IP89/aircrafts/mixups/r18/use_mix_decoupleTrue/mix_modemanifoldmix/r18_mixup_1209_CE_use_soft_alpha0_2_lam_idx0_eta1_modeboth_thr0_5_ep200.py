_base_ = '../../../../../../base.py'
# model settings
model = dict(
    type='MixUpClassification',
    pretrained='work_dirs/my_pretrains/official/resnet18_pytorch.pth',
    alpha=0.2,
    mix_mode="manifoldmix",
    mix_args=dict(
        manifoldmix=dict(layer=(0, 3)),
        resizemix=dict(scope=(0.1, 0.8), use_alpha=True),
        fmix=dict(decay_power=3, size=(224,224), max_soft=0., reformulate=False)
    ),
    backbone=dict(
        type='ResNet_Mix',
        depth=18,
        in_channels=3,
        out_indices=(3,),
        norm_cfg=dict(type='BN')),
    head=dict(
        type='ClsMixupHead',  # mixup head, soft CE decoupled mixup
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0,
            use_soft=True, use_sigmoid=False, use_mix_decouple=True,  # try decouple mixup CE
        ),
        with_avg_pool=True, multi_label=True, two_hot=False, two_hot_scale=1,
        lam_scale_mode='pow', lam_thr=1, lam_idx=0,  # lam rescale
        eta_weight=dict(eta=1, mode="both", thr=0.5),  # decouple mixup
        in_channels=512, num_classes=100)
)

# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')
# Aircrafts
aircrafts_base = "data/FGVC_Aircraft/fgvc-aircraft-2013b/data/"  # IP90
data_train_list = aircrafts_base + 'classification_meta_0/train_labeled.txt'  # labeled train
data_train_root = aircrafts_base
data_test_list = aircrafts_base + 'classification_meta_0/test_labeled.txt'  # labeled test
data_test_root = aircrafts_base

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # imagenet (used in prefetch)
train_pipeline = [
    dict(type='Resize', size=256),
    dict(type='RandomResizedCrop', size=224, scale=[0.5, 1.0]),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=256),
    dict(type='CenterCrop', size=224),
]

# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])
test_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=16,  # try small bs in fine-grained
    workers_per_gpu=4,
    drop_last=True,  # only in fine grained
    train=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_train_list, root=data_train_root,
            **data_source_cfg),
        pipeline=train_pipeline,
        prefetch=prefetch,
    ),
    val=dict(
        type=dataset_type,
        data_source=dict(
            list_file=data_test_list, root=data_test_root, **data_source_cfg),
        pipeline=test_pipeline,
        prefetch=False,
    ))

# additional hooks
custom_hooks = [
    dict(
        type='ValidateHook',
        dataset=data['val'],
        initial=False,
        interval=1,
        imgs_per_gpu=100,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5)))
]

# optimizer
optimizer = dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0005)
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)
checkpoint_config = dict(interval=400)

# runtime settings
total_epochs = 200
