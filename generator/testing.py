from faker import Faker
fake = Faker()
from faker.providers import misc
# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

# create new provider class
class MyProvider(BaseProvider):
    def foo(self) -> str:
        return 'bar'

# then add new provider to faker instance
fake.add_provider(MyProvider)

# now you can use:
fake.foo()
# 'bar'



print(fake.name())
print(fake.providers[7])
fake.add_provider(misc)
print(fake.providers[0])


# 'Lucy Cechtelar'

fake.address()
# '426 Jordy Lodge
#  Cartwrightshire, SC 88120-6700'

fake.text()
# 'Sint velit eveniet. Rerum atque repellat voluptatem quia rerum. Numquam excepturi
#  beatae sint laudantium consequatur. Magni occaecati itaque sint et sit tempore. Nesciunt
#  amet quidem. Iusto deleniti cum autem ad quia aperiam.
#  A consectetur quos aliquam. In iste aliquid et aut similique suscipit. Consequatur qui
#  quaerat iste minus hic expedita. Consequuntur error magni et laboriosam. Aut aspernatur
#  voluptatem sit aliquam. Dolores voluptatum est.
#  Aut molestias et maxime. Fugit autem facilis quos vero. Eius quibusdam possimus est.
#  Ea quaerat et quisquam. Deleniti sunt quam. Adipisci consequatur id in occaecati.
#  Et sint et. Ut ducimus quod nemo ab voluptatum.'