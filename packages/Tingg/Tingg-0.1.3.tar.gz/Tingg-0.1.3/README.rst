Tingg Checkout SDK
===================

.. image:: https://cdn.cellulant.africa/images/brand-assets/tingg-by-cellulant-themed.svg
    :target: https://tingg.africa
    :alt: Tingg by Cellulant
    :height: 64px

Overview
--------

This Tingg Checkout SDK helps you streamline your integration to the Tingg Checkout API to facilitate secure processing of payments. It includes functionality for payload validation and encryption of payment data.

Prerequisites
-------------

You need a `Tingg account <https://app.sandbox.tingg.africa/cas/login>`_ to use this package. If you don't have one you can contact our account managers through `tingg-checkout@cellulant.io` and have your business registered & activated.

Visit our `official documentation <https://docs.tingg.africa/docs/checkout-getting-started>`_ to find out more on how you can get started using Tingg.

Once you're signed in, you will need to retrieve your `API Keys <https://docs.tingg.africa/docs/checkout-getting-started#4--checkout-api-keys>`_, that is the IV Key, the Secret Key, and the Access Key.

Installation
------------

.. code-block:: bash

    pip install Tingg

Usage
-----

.. code-block:: python

    from tingg import Express
    from tingg import Checkout

    payload = {
        # Your payment payload
    }

    iv_key = 'your_iv_key'
    secret_key = 'your_secret_key'
    access_key = 'your_access_key'
    environment = 'sandbox'

    checkout_instance = Checkout(iv_key, secret_key, access_key, environment)
    encrypted_payload, redirect_url = checkout_instance.process_payment(payload)

Features
--------

- Payload Validation: Ensures that the provided payment payload adheres to specified criteria.
- Encryption: Uses AES encryption to secure payment data during processing.

For more detailed usage instructions and examples, refer to the `documentation <https://docs.tingg.africa>`_.

Feedback
--------

Feel free to reach us through our `discussion forum <https://docs.tingg.africa/discuss>`_.
