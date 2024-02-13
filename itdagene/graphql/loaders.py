from typing import Optional
from promise import Promise
from promise.dataloader import DataLoader

from itdagene.app.company.models import Company


class CompanyLoader(DataLoader):
    def batch_load_fn(self, keys) -> Promise:
        def do_work() -> list[Optional[Company]]:
            qs = list(Company.objects.filter(pk__in=keys))

            def get_company(key) -> Optional[Company]:
                return next((x for x in qs if x.pk == key), None)

            return [get_company(key) for key in keys]

        return Promise(lambda resolve, reject: resolve(do_work()))


class Loaders:
    def __init__(self) -> None:
        self.Companyloader = CompanyLoader()
