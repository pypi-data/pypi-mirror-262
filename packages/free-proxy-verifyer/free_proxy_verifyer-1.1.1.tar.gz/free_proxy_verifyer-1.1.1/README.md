free_proxy_verifyer
===========

free_proxy_verifyer is a Python library that allows you to verify whether a proxy is working or not. It checks the functionality of a given proxy by making requests to various proxy detection servers. This library is useful for anyone who needs to ensure the reliability of proxy for their applications.

Installation
------------

You can install free_proxy_verifyer via pip:

`pip install free_proxy_verifyer`

or

`pip install git+https://github.com/mominurr/free_proxy_verifyer.git`

Usage
-----

```
from free_proxy_verifyer import ProxyVerify

# Create an instance of ProxyVerify
checker = ProxyVerify()

# Define the proxy address to be verified
proxy = "37.187.17.89:3128"

# Verify the proxy
result = checker.verify_proxy(proxy=proxy)

# Print the result
print(result)  # True if the proxy is working, else False

```

How it Works
------------

ProxyVerify works by randomly selecting proxy detection services from a predefined list and making requests through the provided proxy. If a response is received within the specified timeout and the status code is 200, it considers the proxy to be working.

Contributing
------------

Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or create a pull request on GitHub.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.