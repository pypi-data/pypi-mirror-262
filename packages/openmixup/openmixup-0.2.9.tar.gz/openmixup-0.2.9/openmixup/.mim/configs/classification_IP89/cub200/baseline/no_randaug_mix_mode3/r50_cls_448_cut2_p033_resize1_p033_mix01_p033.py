_base_ = '../../../../base.py'
# model settings
model = dict(
    type='MixUpClassification',
    alpha=[1, 1, 0.1],
    mix_mode=["cutmix", "resizemix", "mixup"],
    mix_repeat=1,
    mix_args=dict(
        manifoldmix=dict(layer=(0, 3)),
        resizemix=dict(scope=(0.2, 0.8), use_alpha=True),
        fmix=dict(decay_power=3, size=(448,448), max_soft=0., reformulate=False)
    ),
    pretrained='work_dirs/my_pretrains/official/resnet50_pytorch.pth',
    backbone=dict(
        type='ResNet_mmcls',
        depth=50,
        num_stages=4,
        out_indices=(3,),
        style='pytorch'),
    head=dict(
        type='ClsMixupHead', with_avg_pool=True, in_channels=2048, num_classes=200)
)
# dataset settings
data_source_cfg = dict(
    type='ImageNet',
    memcached=False,
    mclient_path='/mnt/lustre/share/memcached_client')

# CUB200
cub_base = "data/CUB200/"
data_train_list = cub_base + 'CUB_200/classification_meta_0/train_labeled.txt'  # labeled train
data_train_root = cub_base + 'CUB_200/images/'
data_test_list = cub_base + 'CUB_200/classification_meta_0/test_labeled.txt'  # labeled test
data_test_root = cub_base + 'CUB_200/images/'

dataset_type = 'ClassificationDataset'
img_norm_cfg = dict(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # imagenet (used in prefetch)
train_pipeline = [
    dict(type='Resize', size=512),  # /0.875
    dict(type='RandomResizedCrop', size=448, scale=[0.5, 1.0]),
    dict(type='RandomHorizontalFlip'),
]
test_pipeline = [
    dict(type='Resize', size=512),
    dict(type='CenterCrop', size=448),
]

# prefetch
prefetch = True
if not prefetch:
    train_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])
test_pipeline.extend([dict(type='ToTensor'), dict(type='Normalize', **img_norm_cfg)])

data = dict(
    imgs_per_gpu=8,  # try small bs in fine-grained
    workers_per_gpu=4,
    drop_last=True,  # only in CUB-200
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
        interval=2,
        imgs_per_gpu=100,
        workers_per_gpu=4,
        eval_param=dict(topk=(1, 5)))
]

# optimizer
optimizer = dict(type='SGD', lr=0.001, momentum=0.9, weight_decay=0.0005,
                paramwise_options={
                    'head': dict(lr=0.01, momentum=0.9)},)  # required parawise_option
optimizer_config = dict(grad_clip=None)

# learning policy
lr_config = dict(policy='CosineAnnealing', min_lr=0.)
checkpoint_config = dict(interval=200)

# runtime settings
total_epochs = 100
