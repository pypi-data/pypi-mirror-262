from setuptools import setup, find_packages

# Read the content of requirements.txt
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='NeuronsMemoryTestPipeline',
    version='0.0.1',
    url='https://gitlab.com/neurons-inc1/data-analyst/neurons_metrics_package',
    install_requires=requirements,
    description="""Root package:
    Package provides QA, MRT and FRT metrics calculation for jatos data obtained from jatos directly or WELD if there are too many participants.
    FRT scores: scores calculation takes into consideration reaction time and group agreement.
    MRT scores consist of two parts: free recall and ad/brand recognition part that mainly incorporates FRT formula to compute the score.
    """,
    author='Irina White, Theo Sell',
    author_email='i.white@neuronsinc.com, t.sell@neuronsinc.com',
    dependency_links=[
        'https://gitlab.com/neurons-inc1/data-analyst/neurons_metrics_package.git#egg=NeuronsMemoryTestPipeline',
    ],
    build_requires=["setuptools", "wheel"],
    include_package_data=True,
    packages=find_packages(),
)