**Magnetic Tile Surface Defect Dataset** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the manufacturing industry, and in the surface defect detection domain. 

The dataset consists of 1344 images with 459 labeled objects belonging to 5 different classes including *blowhole*, *uneven*, *break*, and other: *crack* and *fray*.

Images in the Magnetic Tile Surface Defect dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 956 (71% of the total) unlabeled images (i.e. without annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. Additionally, every image has ***experiment*** tag. The dataset was released in 2018 by the Chinese Academy of Sciences and Columbia University, USA.

<img src="https://github.com/dataset-ninja/magnetic-tile-surface-defect/raw/main/visualizations/poster.png">
