from setuptools import setup, find_packages


VERSION = '0.1.2'
DESCRIPTION = 'Renders 2D Board in console that allows you to change different position in it to different Unicode charecters'

# Setting up
setup(
    name="BoardRendering",
    version=VERSION,
    author="Cybreak",
    author_email="cybreak@cybreak.dev",
    description=DESCRIPTION,
    packages=find_packages(),
    keywords=['python', '2D', 'Console', 'Board Render'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)