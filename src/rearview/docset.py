from __future__ import annotations

import json
import attrs

API_URL = "https://api.zealdocs.org/v1/docsets"
RETRIEVE_URL = "https://go.zealdocs.org/d/{feed}/{name}/latest"

@attrs.frozen
class DocSet:
    source_id: str
    name: str
    title: str
    icon: bytes
    contents: contents.AutoPopulated
    
    @classmethod
    def from_raw(cls, client, raw_data):
        retrieve_url = 
        return cls(
            source_id=raw_data["sourceId"], 
            name=raw_data["name"], 
            title=raw_data["title"],
            icon=base64.b64decode(raw_data["icon"]),
            get_resource=contentlib.make_get_resource(
                name=raw_data["title"],
                client=client, 
                retrieve_url=RETRIEVE_URL.format(
                    feed=raw_data["sourceId"],
                    name=raw_data["name"],
                ),
            ),
        )


@attrs.define
class DocSetCollection:
    _client: cache_client.Client
    _docsets: Mapping[str, DocSet] = attrs.field(init=False, factory=dict)
    
    @classmethod
    def from_client(cls, client):
        return cls(client=client)
    
    async def refresh(self):
        data = await self._client.get(API_URL)
        self._docsets = [
            DocSet.from_raw(self._client, a_set)
            for a_set in json.loads(data)
        ]

    def filter_by_title(self, title_contains):
        title_contains = title_contains.lower()
        for a_docset in self.docsets:
            if title_contains not in a_docset.title.lower():
                continue
            yield a_docset

    def get_by_name(self, name):
        [the_docset] = (
            a_docset
            for a_docset in self.docsets
            if name == a_docset.name
        )
        return the_docset
    
    async def resource(self, resource_path):
        name, resource_path = resource_path.split(resource_path, "/", 1)
        return self.get_by_name(name).get_resource(resource_path)