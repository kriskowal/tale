
from cixar.tale import TaleService
from cixar.ish.lazy import serve, HostService
serve(HostService(TaleService()), port = 2380)

