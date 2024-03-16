from setuptools import find_packages, setup

PACKAGE_NAME = "agent_connector"

# Read the content of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version="0.0.3",
    description="This is my tools package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Micheal Lanham',
    author_email='cxbxmxcx@gmail.com',
    url='https://github.com/cxbxmxcx/Agent-Connector',  # Project homepage URL    
    project_urls={  # Additional URLs as a dictionary
        'Documentation': 'https://github.com/cxbxmxcx/Agent-Connector',
        'Source': 'https://github.com/cxbxmxcx/Agent-Connector',
        'Tracker': 'https://github.com/cxbxmxcx/Agent-Connector/issues',
    },
    packages=find_packages(),
    entry_points={
        "package_tools": ["agent_connector_tool = agent_connector.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
    python_requires='>=3.10',    
)