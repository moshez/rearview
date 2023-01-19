class Options(usage.Options):

    optParameters = [
        ["cache", "c", None, "Location of the cache"],

    def __init__(self):
        self["ports"] = []

    def opt_listen(self, address):
        self["ports"].append(address)

    opt_l = opt_listen

    def postOptions(self):
        if len(self["ports"]) == 0:
            self["ports"].append("tcp:8080")


def makeService(config):
    ret_value = service.MultiService()
    path = pathlib.Path(config["cache"])
    client = cache_client.CacheClient(
        cache_location=path
    )
    collection = DocSetCollection(
        client=client,
    )
    site = server.Site(root)
    for port in config["ports"]:
        svc = strports.service(port, site)
        svc.setServiceParent(ret_value)
    referesher = TimerService(
        call=collection.refresh,
        step=300,
    )
    return ret_value