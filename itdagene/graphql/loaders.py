from promise import Promise
from promise.dataloader import DataLoader

from itdagene.app.company.models import Company


class CompanyLoader(DataLoader):
    def batch_load_fn(self, keys):
        def do_work():
            qs = list(Company.objects.filter(pk__in=keys))

            def get_company(key):
                return next((x for x in qs if x.pk == key), None)

            return [get_company(key) for key in keys]

        return Promise(lambda resolve, reject: resolve(do_work()))


class Loaders:
    def __init__(self):
        self.Companyloader = CompanyLoader()
