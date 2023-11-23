Dataset **Magnetic Tile Surface Defect** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/i/B/15/dWL9rY7EtI260YYtWpv45L0haKYfeHlVyExYHl5LEeTUauTHZdA8xSDROeDW2A2SFNNFoyUpUVTJyo1FISLAatAPA8KDZJptMew2YYAgNUwIsfvf6H4PW2BOnlX7.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Magnetic Tile Surface Defect', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://github.com/abin24/Magnetic-tile-defect-datasets./archive/refs/heads/master.zip).