# TCRembedding/__init__.py
from .version import __version__

def get_embedding_class(embedding_name):
    """
    Dynamically import and return the requested embedding class.
    
    :param embedding_name: The name of the embedding class to import.
    :return: The embedding class.
    """
    if embedding_name in globals():
        return globals()[embedding_name]
    
    try:
        # Construct module and class name strings
        module_name = f".{embedding_name.lower()}.embedding"
        class_name = f"Embedding{embedding_name}"
        
        # Dynamically import the module and class
        module = __import__(module_name, globals(), locals(), [class_name], level=1)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Could not import the {embedding_name} embedding class.") from e

__all__ = ['get_embedding_class', '__version__']
