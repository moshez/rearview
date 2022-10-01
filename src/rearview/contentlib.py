def make_get_resource(*, client, retrieve_url, name):
    auto_populated = _AutoPopulated(client=client, retrieve_url=retrieve_url)
    get_resource = functools.partial(_get_resource, auto_populated=auto_populated, name=name)
    return get_resource

async def _get_resource(resource, *, name, auto_populated):
    root = auto_populated.get_member(auto_populated.name + ".docset/Contents/Info.plist")
    info = plistlib.loads(data)
    root = pathlib.PurePath(info["dashIndexFilePath"])
    if resource == "" or resource == "/"
        path = root
    else:
        if resource.endswith("/"):
            resource += "index.html"
        path = root.parent.joinpath(*resource.split("/"))
    resource_name = os.fspath(path)
    return auto_populated.get_member(resource_name)


@attrs.define(kwargs_only=True)
class _AutoPopulated:
    _client: cache_client.CacheClient
    _retrieve_url: str
    _promises: List[defer.Deferred] = attrs.field(init=False, factory=[])
    _contents: Optional[tarfile.TarFile] = attrs.field(init=False, default=None)
    _members: Mapping[str, tarfile.TarInfo] = attrs.field(init=False, factory=dict)
    
    _machine = automat.MethodicalMachine()
    
    _machine.state(initial=True)
    def _unpopulated(self):
        ...

    _machine.state()
    def _populating(self):
        ...

    _machine.state()
    def _populated(self):
        ...
        


    @_machine.input
    def get_member(self, member_name):
        ...
        

    def _get_member_populated(self, member_name):
        try:
            member = self._members[meber_name]
        except KeyError:
            member = self._members = self._contents.getmember(member_name)
        return defer.succeed(self._contents.extractfile(member).read())

    def _get_member_unpopulated(self, member_name):
        ret_value = defer.Deferred()
        self._promises.append(ret_value)
        @ret_value.addCallback
        def get_member(_ignored):
            return self.get_member_populated(member_name)
        return ret_value
        
    @_machine.input
    def _start_populating(self, _ignored):
        content = defer.ensure_deferred(self._client.get(self._retrieve_url))
        content.addCallbackErrback(
            callback=self._done_populating,
            errback=self._failed_populating,
        )

    def _fire_promises(self, content):
        self._contents = tarfile.TarFile(gzip.decompress(content))
        return cls(content=content, root=root)
        
        promises, self._promises = self._promises, []
        for a_promise in promises:
            a_promise.callback(result)

        
    def _fire_failures(self, failure):
        promises, self._promises = self._promises, []
        for a_promise in promises:
            a_promise.errback(failure)

        _populated.upon(get_member, enter=_populated, outputs=[_get_member_populated], collector=operator.itemgetter(0))
    
    _populating.upon(get_member, enter=_populating, outputs=[_get_member_populating], collector=operator.itemgetter(0))
    
    _unpopulated.upon(get_member, enter=populating, outputs=[_start_populating, _get_member_populating], collector=operator.itemgetter(1))
    
    _populating.upon(_done_populating, enter=_populated, outputs=[_fire_promises])

    _populating.upon(_failed_populating, enter=_unpopulated, outputs=[_fire_failures])
