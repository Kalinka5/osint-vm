from sqlmodel import Field, SQLModel


# Addresses Models
class AddressBase(SQLModel):
    street: str = Field(min_length=1, max_length=256)
    city_id: int | None = Field(default=None, foreign_key='cities.id')
    state: str = Field(default="", max_length=256)
    postal_code: str = Field(default="", max_length=256)
    country_id: int | None = Field(default=None, foreign_key='countries.id')
    type: str = Field(min_length=1, max_length=256)


class Address(AddressBase, table=True):
    __tablename__ = 'addresses'

    id: int | None = Field(default=None, primary_key=True)


class AddressPublic(AddressBase):
    id: int


# Cities Models
class CityBase(SQLModel):
    name: str


class City(CityBase, table=True):
    __tablename__ = 'cities'

    id: int | None = Field(default=None, primary_key=True)


class CityPublic(CityBase):
    id: int


# Companies models
class CompanyBase(SQLModel):
    about: str = Field(min_length=1)
    year_founded: str = Field(default='', max_length=4)
    website: str = Field(max_length=256)
    number_of_employees_id: int = Field(foreign_key='number_of_employees.id')
    linkedin: str | None = Field(default=None, max_length=256)
    facebook: str | None = Field(default=None, max_length=256)
    twitter: str | None = Field(default=None, max_length=256)
    image_id: int = Field(foreign_key='company_images.id')


class Company(CompanyBase, table=True):
    __tablename__ = 'companies'

    id: int | None = Field(default=None, primary_key=True)


class CompanyPublic(CompanyBase):
    id: int


# Company Images models
class CompanyImageBase(SQLModel):
    company_id: int = Field(foreign_key='companies.id')
    image_url: str = Field(default=None, max_length=256)
    image_hash: str = Field(default=None, max_length=256)


class CompanyImage(CompanyImageBase, table=True):
    __tablename__ = 'company_images'

    id: int | None = Field(default=None, primary_key=True)


class CompanyImagePublic(CompanyImageBase):
    id: int


# Countries models
class CountryBase(SQLModel):
    name: str


class Country(CountryBase, table=True):
    __tablename__ = 'countries'

    id: int | None = Field(default=None, primary_key=True)


class CountryPublic(CountryBase):
    id: int


# Industries models
class IndustryBase(SQLModel):
    name: str


class Industry(IndustryBase, table=True):
    __tablename__ = 'industries'

    id: int | None = Field(default=None, primary_key=True)


class IndustryPublic(IndustryBase):
    id: int


# Number of employees models
class NumberOfEmployeesBase(SQLModel):
    name: str


class NumberOfEmployees(NumberOfEmployeesBase, table=True):
    __tablename__ = 'number_of_employees'

    id: int | None = Field(default=None, primary_key=True)


class NumberOfEmployeesPublic(NumberOfEmployeesBase):
    id: int
