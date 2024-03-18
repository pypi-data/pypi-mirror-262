class StorefrontApiViewsProductError(Exception):
    pass


class ViewConfigurationError(StorefrontApiViewsProductError):
    pass


class InvalidDataError(StorefrontApiViewsProductError):
    pass


class ConfigurationError(Exception):
    pass
