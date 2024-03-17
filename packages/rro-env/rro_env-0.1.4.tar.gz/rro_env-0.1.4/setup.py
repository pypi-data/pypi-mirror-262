from setuptools import setup, find_packages

setup(
    name='rro_env',
    version='0.1.4',
    packages=find_packages(),
    install_requires=['gymnasium', 'numpy', 'joblib', 'pandas', 'tqdm', 'dill', 'cachetools'],
    author="Near Yip",
    author_email="yiptsangkin@gmail.com",
    description="A Gym environment for 3D container relocation",
    keywords="CRP, 3D, container relocation, RL, gym, environment",
    url="https://github.com/JNU-Tangyin/RRO",
)