from setuptools import find_packages, setup

with open("version") as fd:
    version = fd.read().strip()

with open("README.md") as f:
    README = f.read()


def _load_requirements(filename):
    with open(filename) as fd:
        reqs = [dependency.strip() for dependency in fd if dependency.strip()]
    return [r for r in reqs if not r.startswith(("file://", "#", "--", "-c"))]


dev_requirements = _load_requirements("dev-requirements.txt")


setup(
    name="storefront-api-views-product",
    version=version,
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Intended Audience :: Developers",
    ],
    author="DSCBE",
    author_email="en-dsc-be@takealot.com",
    url="https://github.com/TAKEALOT/storefront-api-views-product",
    packages=find_packages(),
    test_suite="tests",
    install_requires=[
        "typing-extensions",
        "storefront-product-adapter >= 2.0.0",
        "storefront-media-urls >= 1.0.0",
    ],
    extras_require={"dev": dev_requirements},
    package_data={
        "storefront_api_views_product": ["py.typed"],
    },
)
