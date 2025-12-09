import pkgutil
import inspect
from pathlib import Path
from typing import Dict, Type
from .base_metric import BaseMetric

# A registry to hold all the discovered metric classes
METRIC_REGISTRY: Dict[str, Type[BaseMetric]] = {}

def _discover_metrics():
    """
    Dynamically discovers and registers all metric classes in this directory.
    It skips abstract base classes like BaseMetric and RatioMetric.
    """
    package_path = Path(__file__).parent
    for _, name, _ in pkgutil.iter_modules([str(package_path)]):
        module = __import__(f"{__name__}.{name}", fromlist=["*"])
        for _, cls in inspect.getmembers(module, inspect.isclass):
            # Check if the class is a subclass of BaseMetric, but not BaseMetric itself,
            # and importantly, is not an abstract class.
            if issubclass(cls, BaseMetric) and cls is not BaseMetric and not inspect.isabstract(cls):
                # Instantiate the class to get the metric_name
                instance = cls()
                if instance.metric_name != "base_metric":
                    METRIC_REGISTRY[instance.metric_name] = cls
        print(METRIC_REGISTRY)
# Run discovery when the package is imported
_discover_metrics()

def get_metric_config(metric_name: str) -> Type[BaseMetric]:
    """
    Returns the metric configuration class for the given metric name.
    """
    return METRIC_REGISTRY.get(metric_name)
