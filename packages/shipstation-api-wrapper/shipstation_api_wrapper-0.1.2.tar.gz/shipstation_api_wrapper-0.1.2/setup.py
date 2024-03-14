# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shipstation_api_wrapper', 'shipstation_api_wrapper.models']

package_data = \
{'': ['*']}

install_requires = \
['email-validator>=2.1.1,<3.0.0',
 'pydantic[email]>=2.6.3,<3.0.0',
 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'shipstation-api-wrapper',
    'version': '0.1.2',
    'description': 'Non official Shipstation API wrapper',
    'long_description': '## Description:\nThis Python package serves as a comprehensive wrapper for the ShipStation API, designed to simplify the integration of ShipStation\'s shipping, fulfillment, and order management functionalities into your Python applications. By abstracting the complexities of direct API calls, this wrapper provides an intuitive interface for developers to interact with ShipStation, making it easier to automate shipping operations, manage orders, and streamline logistics processes directly from Python code.\n\n## Features\n\n- **Easy Configuration**: Set up your API keys once, and you\'re ready to interact with all available endpoints.\n- **Order Management**: Retrieve, filter, and manage orders with simple method calls.\n- **Shipment Handling**: List and update shipment details effortlessly.\n- **Customer Insights**: Access and manage customer information, including filtering by specific criteria.\n- **Customs Declarations**: Simplify international shipping with easy customs declaration updates.\n- **Tag Management**: Apply tags to orders for easy organization and tracking.\n- **Comprehensive Filters**: Utilize built-in filtering to easily manage and search through orders and shipments based on custom criteria.\n\n## Installation:\n\nInstall the package using pip:\n\n```bash\npip install shipstation-api-wrapper\n```\n\n## Getting Started: \n\n```python\nfrom shipstation_api_wrapper.api import ShipStationClient\n\napi_key = \'your_api_key_here\'\nclient = ShipStationClient(api_key)\n\n```\n\n## Basic Usage: \n\n### Orders\n- Retrieve an order by ID: \n\n```py\norder = client.orders.get_by_id(order_id="123456")\nprint(order.json())\n```\n\n- List orders with custom filtering\n```py\nfrom shipstation_api_wrapper.filter import ShipStationOrderFilter\n\norder_filter = ShipStationOrderFilter()\norder_filter.add_order_number("1001")\norders = client.orders.list_with_filter(order_filter=order_filter)\nprint(orders.json())\n```\n\n## Advanced Features\nRefer to the ShipStation API Documentation for more details on the advanced usage of the API.\n\n## Contributing\nI welcome contributions from the community! Please refer to the project\'s contributing guidelines for more information.\n',
    'author': 'Vick Mu',
    'author_email': 'arbi3400@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
