import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()


class CustomInstallCommand(install):
    def run(self):
        install.run(self)

        # Add the installation directory to PATH
        install_dir = os.path.join(self.install_scripts, '')
        self._update_path(install_dir)

    def _update_path(self, install_dir):
        # Check if the directory is not in PATH
        if install_dir not in os.environ['PATH']:
            print(f"Adding '{install_dir}' to PATH.")

            # Update the PATH using environ
            os.environ['PATH'] += f";{install_dir}"

            # Save changes to the current shell
            with open(os.path.expanduser('~/.bashrc'), 'a') as f:
                f.write(f"export PATH=$PATH:{install_dir}\n")

            # Apply changes to the current shell
            os.system("source ~/.bashrc")


setup(
    name='ayapingping-py',
    version='4.3.10',
    python_requires='>=3.10.12',
    author='Dali Kewara',
    author_email='dalikewara@gmail.com',
    description='ayapingping-py generates standard project structure to build applications in Python that follow Clean '
                'Architecture and Feature-Driven Design concept',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords=['python', 'ayapingping', 'ayapingping-py', 'framework', 'structure', 'design', 'feature', 'project',
              'clean-architecture', 'feature-driven-design', 'domain-driven-design'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=find_packages(),
    cmdclass={'install': CustomInstallCommand},
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ayapingping-py = _main.main:main',
        ],
    },
)
