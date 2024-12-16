_base_ = [
    '../_base_/models/faster-rcnn_r50_fpn.py',
    '../_base_/datasets/coco_detection.py',
    '../_base_/schedules/schedule_1x.py',
    '../_base_/default_runtime.py'
]

# Define the optimizer in the config
optimizer = dict(
    type='Adam',
    lr=0.0001,  # You can adjust the learning rate based on your needs
    weight_decay=0.0001  # Typically a small weight decay to avoid overfitting
)

# Define the learning rate scheduler (optional)
lr_config = dict(
    policy='step',
    step=[30, 40],  # Change the step according to the number of epochs
    gamma=0.1
)

# Keep the rest of the model and training config as it is


# Paths for data
data_root = '/kaggle/working/JHU-CROWD++-2/'

# Define train, validation, and test dataloaders
train_dataloader = dict(
    batch_size=1,
    dataset=dict(
        ann_file=data_root + 'train/_annotations.coco.json',
        data_prefix=dict(img=data_root + 'train/'),
        metainfo=dict(
            classes=('head',),  # Replace with your class name(s)
            palette=[(220, 20, 60)],  # RGB colors for visualization
        ),
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations', with_bbox=True),
            dict(type='Resize', scale=(200, 200), keep_ratio=True),  # Resize images to 640x640
            dict(type='RandomFlip', prob=0.5),
            dict(type='PackDetInputs')
        ]
    )
)

val_dataloader = dict(
    dataset=dict(
        ann_file=data_root + 'valid/_annotations.coco.json',
        data_prefix=dict(img=data_root + 'valid/'),
        metainfo=dict(
            classes=('head',),
            palette=[(220, 20, 60)],
        ),
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='Resize', scale=(200, 200), keep_ratio=True),  # Resize images to 640x640
            dict(
                type='PackDetInputs',
                meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape', 'scale_factor')
            )
        ]
    )
)

test_dataloader = dict(
    dataset=dict(
        ann_file=data_root + 'test/_annotations.coco.json',
        data_prefix=dict(img=data_root + 'test/'),
        metainfo=dict(
            classes=('head',),
            palette=[(220, 20, 60)],
        ),
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='Resize', scale=(640, 640), keep_ratio=True),  # Resize images to 640x640
            dict(
                type='PackDetInputs',
                meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape', 'scale_factor')
            )
        ]
    )
)

# Define evaluators for validation and testing
val_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'valid/_annotations.coco.json',
    metric=['bbox']
)

test_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'test/_annotations.coco.json',
    metric=['bbox']
)

# Update model configuration
model = dict(
    roi_head=dict(
        bbox_head=dict(
            num_classes=1  # Number of classes in your dataset
        )
    )
)

# Default hooks
default_hooks = dict(
    checkpoint=dict(interval=5),
)

# Training configuration
train_cfg = dict(max_epochs=50)


# Directory to save outputs
work_dir = '/kaggle/working/faster_rcnn_jhu_crowd'
