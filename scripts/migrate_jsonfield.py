from datamodels.products.models import mm_Product
from datamodels.stores.models import mm_Store


def run():
    print('migrate products star...')
    mm_Product.update(images='')
    print('migrate product done.')

    print('migrate store start...')
    mm_Store.update(images='')
    print('migrate store done.')

