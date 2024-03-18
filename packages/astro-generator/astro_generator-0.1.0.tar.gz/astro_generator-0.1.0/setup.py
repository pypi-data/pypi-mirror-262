from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="astro_generator",
    python_requires=">=3.9",
    version="0.1.0",
    packages=find_packages(),
    license="GNU General Public License v3.0",
    description="A library providing simple methods of generating random but semi-realistic data of fictional celestial bodies.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Zitronenjoghurt",
    extras_require={'dev': ['pytest', 'twine', 'wheel']},
    url="https://github.com/Zitronenjoghurt/AstroGenerator"
)