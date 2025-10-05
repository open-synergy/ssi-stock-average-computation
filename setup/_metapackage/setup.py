import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-stock-average-computation",
    description="Meta package for open-synergy-ssi-stock-average-computation Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_stock_average_computation',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
