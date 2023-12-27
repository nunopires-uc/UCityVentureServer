class User:
    def __init__(self, email="", id="", nome="", numRatings=0, somaRatings=0.0):
        self.email = email
        self.id = id
        self.nome = nome
        self.numRatings = numRatings
        self.somaRatings = somaRatings

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def numRatings(self):
        return self._numRatings

    @numRatings.setter
    def numRatings(self, value):
        self._numRatings = value

    @property
    def somaRatings(self):
        return self._somaRatings

    @somaRatings.setter
    def somaRatings(self, value):
        self._somaRatings = value

    def __str__(self):
        return f"User(email='{self.email}', id='{self.id}', nome='{self.nome}', numRatings={self.numRatings}, somaRatings={self.somaRatings})"
