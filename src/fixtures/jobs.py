import factory
from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory
from decimal import Decimal


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker("pyint")
    title = factory.Faker("job")
    description = factory.Faker("pystr")
    salary_from = factory.Faker("pydecimal", right_digits=2, positive=True, max_value=100000000)
    salary_to = factory.LazyAttribute(lambda job: job.salary_from*Decimal(1.1))
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
