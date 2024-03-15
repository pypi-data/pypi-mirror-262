from setuptools import find_packages, setup
setup(
    name="preprocess-xsoar",
    version ="0.1",
    packages =find_packages(),
    py_modules =["preprocess_utils.mapper","preprocess_utils.models.action","preprocess_utils.models.alert",
                 "preprocess_utils.models.demisto","preprocess_utils.models.event","preprocess_utils.models.extensions",
                 "preprocess_utils.models.service","preprocess_utils.models.severity","preprocess_utils.models.ticket_action",
                 "preprocess_utils.transformers.__init__","preprocess_utils.transformers.country","preprocess_utils.transformers.date","preprocess_utils.transformers.ip"])