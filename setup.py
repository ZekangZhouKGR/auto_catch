from setuptools import setup,find_packages
import auto_catch

setup(
    name = auto_catch.__application__,
    version = auto_catch.__version__,
    packages = find_packages(),
    package_data = {
        'auto_catch':['']
    },
    author_email = "thisisaspider@gmail.com",
    description = "自动截图插件",
    url = None,
    entry_points = {
        'console_scripts':[
        ]
    },
    install_requires = [
    ],
    long_description = open("README.md","r", encoding='utf-8').read(),
    long_description_content_type = "text/markdown",
    python_requires = ">=3.6"
    # test_suite = 'auto_catch.test'
)