from setuptools import setup, find_packages

setup(
    name='convertfiletovoice2',
    version='0.1',
    packages=find_packages(),
    description='convert file to voice',
    author='MarkoKoval <marko.koval.work@gmail.com>',
    install_requires=[            # I get to this in a second
          'pyttsx3',
    ],
)

# pip install setuptools wheel twine
# python setup.py sdist bdist_wheel
# twine upload dist/*

# export TWINE_USERNAME=__token__
# export TWINE PASSWORD=pypi-AgEIcHlwaS5vcmcCJDFhYzg1MDhlLTIyMGMtNDYxOC1hMGE4LTk5MTRhYzljYjUxNAACKlszLCI2NWNkOGIyYi01MzM1LTRhYTUtOGM5Zi1jYjIxOGRhNTY2MGYiXQAABiBa99I_PcNm2mAx3PB8TVEO2UgRRJbdrLWaqVc0kzagzw