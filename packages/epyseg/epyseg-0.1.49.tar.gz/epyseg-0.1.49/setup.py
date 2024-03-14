import setuptools
# from epyseg.epygui import __AUTHOR__, __VERSION__, __EMAIL__
from epyseg.version import __VERSION__,__EMAIL__,__AUTHOR__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='epyseg',
    version=__VERSION__,
    author=__AUTHOR__,
    author_email=__EMAIL__,
    description='A deep learning based tool to segment epithelial tissues. The epyseg GUI can be uesd to build, train or run custom networks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/baigouy/EPySeg',
    package_data={'': ['*.md','*.json','deeplearning/zoo/*/*.*','deeplearning/zoo/*/*/*.*']}, # the two last entries allow to include third party models as pb that should be portable irrespective of the version of tf...
    license='BSD',
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    # TODO put this in requirements.txt file and read the file from here --> can have both methods work
    # below are the required files (they will be installed together with epyseg unless the '--no-deps' tag is used)
    install_requires=[
        # "tensorflow>=2.0.0",  # to allow for mac OS X conda support #shall I put 2.3 now
        # "tensorflow-gpu>=2.0.0;platform_system!='Darwin'",
        # "tensorflow>=2.3.1", # pb 2.3.1 is not supported in python 3.8 and there is a pb accessing the layers --> I need a fix but maybe ok for now # I have a modulewrapper bug with tf 2.7.1 --> so until I understand it I will rely on that version TODO should I add ;platform_system=='Darwin' ? --> try it # to allow for mac OS X conda support #shall I put 2.3 now # current collab version is 2.8
        "tensorflow<2.16.0", # somehow tf 2.16 has a pb!!! # pb 2.3.1 is not supported in python 3.8 and there is a pb accessing the layers --> I need a fix but maybe ok for now # I have a modulewrapper bug with tf 2.7.1 --> so until I understand it I will rely on that version TODO should I add ;platform_system=='Darwin' ? --> try it # to allow for mac OS X conda support #shall I put 2.3 now # current collab version is 2.8
        # "tensorflow==2.15.0", # somehow tf 2.16 has a pb!!! # pb 2.3.1 is not supported in python 3.8 and there is a pb accessing the layers --> I need a fix but maybe ok for now # I have a modulewrapper bug with tf 2.7.1 --> so until I understand it I will rely on that version TODO should I add ;platform_system=='Darwin' ? --> try it # to allow for mac OS X conda support #shall I put 2.3 now # current collab version is 2.8
        # "tensorflow-gpu>=2.3.1;platform_system!='Darwin'", # tensorflow-gpu==2.3.1 # do I still need to exclude macOS??? --> pb is old macs maybe # apparently this line is useless now and there is no point in having it because tensorflow uses the gpu by default if it's there and properly congigured !
        "segmentation-models==1.0.1",
        # "tensorflow-gpu>=2.0.0", # not required ? # make sure it does not install on OS X to prevent crash if does not exist # tf-gpu seems deprecated anyways...
        "czifile",
        # "h5py", # should be installed with tensorflow gpu so do I need it ??? # probably better to remove it to avoid intsalling erroneous versions that are incompatible with tensorflow... similarly do I really need to have numpy it will be installed with tf anyways??? --> just try
        "Markdown",
        "matplotlib>=3.5.2", #  required to have matplotlib support of pyqt6 --> which will be used by default in the future
        "numpy",
        # "numpydoc", # not needed any longer
        "Pillow>=8.1.2", # because there are security issues with below
        # for now intsall both but soon just rely on pyqt6 ???
        "PyQt5", # PyQt5==5.15.4    PyQt5-Qt5==5.15.2 # check versions are ok!!!
        # "PyQtWebEngine", #PyQtWebEngine==5.15.4 PyQtWebEngine-Qt5==5.15.2  # removed because it cause several bugs to the soft and is sometimes hard to install
        "PyQt6", # PyQt5==5.15.4    PyQt5-Qt5==5.15.2 # check versions are ok!!! # may require: sudo apt install qt6-base-dev
        # "PyQt6-WebEngine", #PyQtWebEngine==5.15.4 PyQtWebEngine-Qt5==5.15.2 # removed because it cause several bugs to the soft and is sometimes hard to install
        "read-lif",
        "scikit-image>=0.19.3", #scikit-image>=0.18.1 # 0.19.3 is required for applying 3D affine trafo
        "scipy>=1.7.3", # scipy==1.6.3 # 1.7.3 is required for applying 3D affine trafo
        "scikit-learn>=1.0.2",  # for pyTA contour sorting deprecated (remove ?) # 1.0.2 is required for applying 3D affine trafo now
        "tifffile>=2021.11.2", #tifffile==2021.11.2 # ok bug is now fixed --> can keep all the versions of tifffile! # NB apparently there is a bug with the latest version for saving as imageJ (with metadata) --> I may need fix the version to 2021.11.2 # but try it
        "tqdm",
        "natsort",
        "numexpr",
        "urllib3", # for model download
        "qtawesome", # for the TA icons
        "pandas", #pandas==0.24.2n
        "numba", #numba==0.48.0
        "elasticdeform", # a library to further increase the range of data aug
        "roifile", # for support of IJ ROIs soon
        "prettytable", # for SQL preview in pyTA
        "pyperclip", # for pyta lists
        "QtPy>=2.1.0", # from now on this is how I would handle the pyqt/pyside integration
        # "aicsimageio", # new library t oread czi files (or any file maybe ????)--> replace my entire Img library ???
        # "aicspylibczi>=3.0.5", # required for the above to read czi files !!!
        # "pylibczi", # deprecated --> replaced by the 2 above --> DO NOT USE
        # "pylibCZIrw" # --> a python wrapper for libCZI --> this is the Zeiss made stuff so -> SO COOL
        # "parameterized",#required for unit tests
        # "sympy" # TODO add this if I finally use it in EZF
        # six==1.15.0,
        # "cython",
        # "cooltools",
        # "cooler",
        #

        # "keras",# nb it seems I need install keras because of segmentation models (deprecated calls), the only pb is that i need to install the matching version to tensorflow to avoid issues is there a way to do that -−> OR MAYBE DO A YAML AND FREEZE VERSIONS
        # "liftover", # to be added soon
        # "pygneometracks", # to be added soon
        # "biopython", #  to be added soon
    ],

    # !python --version # to check python version in colab

    # extras_require = {
    #     'all':  ["tensorflow-gpu>=2.0.0"]
    # },
    # python_requires='>=3.6, <3.9' #  --> could put < 3.10 but then I would have to change tf version to 2.5 and I haven't tested it (see https://www.tensorflow.org/install/pip?hl=fr) --> should try that first --> check the colba version to see if that works or not !!!
    # python_requires='>=3.6, <3.10' # from 16/03/23 tensorflow is now supported by python 3.9 and tf version is 2.11.0 --> could put < 3.10 but then I would have to change tf version to 2.5 and I haven't tested it (see https://www.tensorflow.org/install/pip?hl=fr) --> should try that first --> check the colba version to see if that works or not !!!
    python_requires='>=3.6, <3.11' # from 04/05/23 colab is using python 3.10.11
    # NB colab uses tf 2.8.0 by default (date = 16/02/22) (https://colab.research.google.com/notebooks/tensorflow_version.ipynb#scrollTo=-XbfkU7BeziQ) --> see if my tool works with that then update
    # python version on colab is 3.7.12 --> therefore it is really worth keeping it that way (import sys  sys.version)
)

# to test with testpy !pip install --no-deps -i https://test.pypi.org/simple/ epyseg==0.1.30

# pip3 freeze # the versions have changed --> try with a fresh install just to see if that works

# TODO add svg libs ???
# my versions in case that's needed some day
# should I add keras for seg models ???
# czifile==2019.7.2
# h5py==2.9.0
# Markdown==3.1.1
# matplotlib==3.1.3
# numpy==1.16.4
# numpydoc==0.9.2
# Pillow==7.0.0
# PyQt5==5.13.0
# PyQtWebEngine==5.13.0
# read-lif==0.2.1
# scikit-image==0.16.2
# scipy==1.4.1
# segmentation-models==1.0.1
# tensorflow==2.1.0
# tensorflow-gpu==2.1.0
# tifffile==2020.2.16
# tqdm==4.42.1
# natsort=7.0.1
# numexpr=2.7.1