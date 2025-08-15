Dataset **Magnetic Tile Surface Defect** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMzAzN19NYWduZXRpYyBUaWxlIFN1cmZhY2UgRGVmZWN0L21hZ25ldGljLXRpbGUtc3VyZmFjZS1kZWZlY3QtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAibVZ3R3AybXZtK2RuZlFaY0hOZFlGOEtLRlpYeC96U2Z6MzFnNmk4ajYyOD0ifQ==?response-content-disposition=attachment%3B%20filename%3D%22magnetic-tile-surface-defect-DatasetNinja.tar%22)

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