

from .base import BaseEmbeddings


class CustomEmbeddings(BaseEmbeddings):
    """
    TODO: Replace with custom embedding model
    """
    def run(self, text, *args, **kwargs):
        return super().run(text, *args, **kwargs)
    
