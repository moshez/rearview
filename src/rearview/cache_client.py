from __future__ import annotation

import hashlib
from treq import client

@attrs.frozen
class CachingClient:
    _cache_location: pathlib.Path
    _treq: treq.client.HTTPClient = attr.field(factory=treq.client.HTTPClient)
    
    async def get(self, url):
        cleaned = url.replace("/", "_")
        hashed = hashlib.sha256.update(url.encode("utf-8")).hexdigest()
        name = cleaned + "_" + hashed
        location = self._cache_location / name
        try:
            return location.read_bytes()
        except FileNotFoundError:
            pass
        response = await self._treq.get(url)
        if response.code != 200:
            raise ValueError("bad response", response)
        content = await response.content()
        temp_location = location.parent / (name + ".tmp")
        temp_location.write_bytes(content)
        return content
    
    @classmethod
    def from_path(cls, path):
        return cls(treq=client.HTTPClient(), _cache_location=pathlib.Path(path))
