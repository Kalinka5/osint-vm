from enum import Enum

from fastapi import FastAPI, HTTPException
from sqlmodel import select

from fastapi_pagination import Page, add_pagination, paginate

from database import SessionDep
from models import *


class Tags(Enum):
    addresses = 'Addresses'
    cities = 'Cities'
    companies = 'Companies'
    countries = 'Countries'
    industries = 'Industries'
    number_of_employees = 'Number of employees'


app = FastAPI()
add_pagination(app)


@app.post('/addresses/', response_model=AddressPublic, status_code=201, tags=[Tags.addresses], summary="Create an address")
async def create_address(address: AddressBase, session: SessionDep):
    """Create an address with all information: 

    - **street**: each address must have a street (required)
    - **city_id**: city id from "cities" table (not required)
    - **state**: state of your address (not required)
    - **postal_code**: postal code number of your address (not required)
    - **country_id**: country id from "countries" table (not required)
    - **type**: it can be "headquarters" or "others" (required)
    """
    # Check if the city_id exists if provided
    if address.city_id:
        city = session.get(City, address.city_id)
        if not city:
            raise HTTPException(
                status_code=400, detail="Invalid city_id: City does not exist")

    # Check if the country_id exists if provided
    if address.country_id:
        country = session.get(Country, address.country_id)
        if not country:
            raise HTTPException(
                status_code=400, detail="Invalid country_id: Country does not exist")

    db_address = Address.model_validate(address)
    session.add(db_address)
    session.commit()
    session.refresh(db_address)

    return db_address


@app.get('/addresses/', tags=[Tags.addresses], summary="Get all addresses")
async def read_addresses(session: SessionDep) -> Page[AddressPublic]:
    """Retrieve a paginated list of all addresses. You can choose page and how many addresses will be displayed in each page"""
    addresses = session.exec(select(Address)).all()

    return paginate(addresses)


@app.get('/addresses/{Address_id}', response_model=AddressPublic, tags=[Tags.addresses], summary="Get an address by id")
async def get_address(address_id: int, session: SessionDep):
    """Retrieve an address information by its ID:

    - **address_id**: The ID of the address to retrieve.
    """
    address = session.get(Address, address_id)

    if not address:
        raise HTTPException(status_code=404, detail="address not found")

    return address


@app.patch('/addresses/{address_id}', response_model=AddressPublic, tags=[Tags.addresses], summary="Update an address by id")
async def update_address(address_id: int, address: AddressBase, session: SessionDep):
    """Change full information about current address:

    - **street**: each address must have a street (required)
    - **city_id**: city id from "cities" table (not required)
    - **state**: state of your address (not required)
    - **postal_code**: postal code number of your address (not required)
    - **country_id**: country id from "countries" table (not required)
    - **type**: it can be "headquarters" or "others" (required)

    **!!! IMPORTANT: Fill in ALL fields of address, because it updates FULL information**
    """
    address_db = session.get(Address, address_id)

    if not address_db:
        raise HTTPException(status_code=404, detail="Address not found")

    address_data = address.model_dump(exclude_unset=True)
    address_db.sqlmodel_update(address_data)
    session.add(address_db)
    session.commit()
    session.refresh(address_db)

    return address_db


@app.delete('/addresses/{address_id}', status_code=204, tags=[Tags.addresses], summary="Delete an address by id")
async def delete_address(address_id: int, session: SessionDep):
    """Delete full address information from database by ID:

    - **address_id**: The ID of the address to delete.
    """
    address = session.get(Address, address_id)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    session.delete(address)
    session.commit()

    return {"ok": True}


@app.post('/cities/', response_model=CityPublic, status_code=201, tags=[Tags.cities], summary="Create a city")
async def create_city(city: CityBase, session: SessionDep):
    """Create a city with name value: 

    - **name**: each city must have a name (required)
    """
    db_city = City.model_validate(city)
    session.add(db_city)
    session.commit()
    session.refresh(db_city)

    return db_city


@app.get('/cities/', tags=[Tags.cities], summary="Get all cities")
async def read_cities(session: SessionDep) -> Page[CityPublic]:
    """Retrieve a paginated list of all cities. You can choose page and how many cities will be displayed in each page"""
    cities = session.exec(select(City)).all()

    return paginate(cities)


@app.get('/cities/{city_id}', response_model=CityPublic, tags=[Tags.cities], summary="Get a city by id")
async def get_city(city_id: int, session: SessionDep):
    """Retrieve a city information by its ID:

    - **city_id**: The ID of the city to retrieve.
    """
    city = session.get(City, city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@app.patch('/cities/{city_id}', response_model=CityPublic, tags=[Tags.cities], summary="Update a city by id")
async def update_city(city_id: int, city: CityBase, session: SessionDep):
    """Change name information about current city:

    - **name**: each city must have a name (required)
    """
    city_db = session.get(City, city_id)

    if not city_db:
        raise HTTPException(status_code=404, detail="City not found")

    city_data = city.model_dump(exclude_unset=True)
    city_db.sqlmodel_update(city_data)
    session.add(city_db)
    session.commit()
    session.refresh(city_db)

    return city_db


@app.delete('/cities/{city_id}', status_code=204, tags=[Tags.cities], summary="Delete a city by id")
async def delete_city(city_id: int, session: SessionDep):
    """Delete full city information from database by ID:

    - **city_id**: The ID of the city to delete.
    """
    city = session.get(City, city_id)

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    session.delete(city)
    session.commit()

    return {"ok": True}


@app.post("/companies/", response_model=CompanyPublic, status_code=201, tags=[Tags.companies], summary="Create a company")
async def create_company(company: CompanyBase, session: SessionDep):
    """Create a company with all information:

    - **about**: small information about company (required)
    - **year_founded**: year when company was founded (not required)
    - **website**: company's website link (required)
    - **number_of_employees_id**: number of employees ID from "number_of_employees" table (required)
    - **linkedin**: link to company's LinkedIn account (not required)
    - **facebook**: link to company's Facebook account (not required)
    - **twitter**: link to company's Twitter account (not required)
    """
    if company.number_of_employees_id:
        number_id = session.get(
            NumberOfEmployees, company.number_of_employees_id)
        if not number_id:
            raise HTTPException(
                status_code=400, detail="Invalid number_of_employees_id: Number of employees does not exist")

    db_company = Company.model_validate(company)
    session.add(db_company)
    session.commit()
    session.refresh(db_company)

    return db_company


@app.get("/companies/", tags=[Tags.companies], summary="Get all companies")
async def read_companies(session: SessionDep) -> Page[CompanyPublic]:
    """Retrieve a paginated list of all companies. You can choose page and how many companies will be displayed in each page"""
    # Filter companies where the favicon column is not null
    companies_query = select(Company).where(Company.favicon.is_not(None))
    companies = session.exec(companies_query).all()

    return paginate(companies)


@app.get("/companies/{company_id}", response_model=CompanyPublic, tags=[Tags.companies], summary="Get a company by id")
async def get_company(company_id: int, session: SessionDep):
    """Retrieve a company information by its ID:

    - **company_id**: The ID of the company to retrieve.
    """
    company = session.get(Company, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return company


@app.patch('/companies/{company_id}', response_model=CompanyPublic, tags=[Tags.companies], summary="Update a company by id")
async def update_company(company_id: int, company: CompanyBase, session: SessionDep):
    """Change full information about current company:

    - **about**: small information about company (required)
    - **year_founded**: year when company was founded (not required)
    - **website**: company's website link (required)
    - **number_of_employees_id**: number of employees ID from "number_of_employees" table (required)
    - **linkedin**: link to company's LinkedIn account (not required)
    - **facebook**: link to company's Facebook account (not required)
    - **twitter**: link to company's Twitter account (not required)

    **!!! IMPORTANT: Fill in ALL fields of company, because it updates FULL information**
    """
    company_db = session.get(Company, company_id)

    if not company_db:
        raise HTTPException(status_code=404, detail="Company not found")

    company_data = company.model_dump(exclude_unset=True)
    company_db.sqlmodel_update(company_data)
    session.add(company_db)
    session.commit()
    session.refresh(company_db)

    return company_db


@app.delete("/companies/{company_id}", status_code=204, tags=[Tags.companies], summary="Delete a company by id")
def delete_company(company_id: int, session: SessionDep):
    """Delete full company information from database by ID:

    - **company_id**: The ID of the company to delete.
    """
    company = session.get(Company, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    session.delete(company)
    session.commit()

    return {"ok": True}


@app.post('/countries/', status_code=201, response_model=CountryPublic, tags=[Tags.countries], summary="Create a country")
async def create_country(country: CountryBase, session: SessionDep):
    """Create a country with name value:

    - **name**: each country must have name (required)
    """
    db_country = Country.model_validate(country)
    session.add(db_country)
    session.commit()
    session.refresh(db_country)

    return db_country


@app.get('/countries/', tags=[Tags.countries], summary="Get all countries")
async def read_countries(session: SessionDep) -> Page[CountryPublic]:
    """Retrieve a paginated list of all countries. You can choose page and how many countries will be displayed in each page"""
    countries = session.exec(select(Country)).all()

    return paginate(countries)


@app.get('/countries/{country_id}', response_model=CountryPublic, tags=[Tags.countries], summary="Get a country by id")
async def get_country(country_id: int, session: SessionDep):
    """Retrieve a country information by its ID:

    - **country_id**: The ID of the country to retrieve.
    """
    country = session.get(Country, country_id)

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    return country


@app.patch("/countries/{country_id}", response_model=CountryPublic, tags=[Tags.countries], summary="Update a country by id")
def update_country(country_id: int, country: CountryBase, session: SessionDep):
    """Change name information about current country:

    - **name**: each country must have name (required)
    """
    country_db = session.get(Country, country_id)

    if not country_db:
        raise HTTPException(status_code=404, detail="Country not found")

    country_data = country.model_dump(exclude_unset=True)
    country_db.sqlmodel_update(country_data)
    session.add(country_db)
    session.commit()
    session.refresh(country_db)

    return country_db


@app.delete("/countries/{country_id}", status_code=204, tags=[Tags.countries], summary="Delete a country by id")
def delete_country(country_id: int, session: SessionDep):
    """Delete full country information from database by ID:

    - **country_id**: The ID of the country to delete.
    """
    country = session.get(Country, country_id)

    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    session.delete(country)
    session.commit()

    return {"ok": True}


@app.post('/industries/', status_code=201, response_model=IndustryPublic, tags=[Tags.industries], summary="Create an industry")
async def create_industry(industry: IndustryBase, session: SessionDep):
    """Create an industry with name value:

    - **name**: each industry must have name (required)
    """
    db_industry = Industry.model_validate(industry)
    session.add(db_industry)
    session.commit()
    session.refresh(db_industry)

    return db_industry


@app.get('/industries/', tags=[Tags.industries], summary="Get all industries")
async def read_industries(session: SessionDep) -> Page[IndustryPublic]:
    """Retrieve a paginated list of all industries. You can choose page and how many industries will be displayed in each page"""
    industries = session.exec(select(Industry)).all()

    return paginate(industries)


@app.get('/industries/{industry_id}', response_model=IndustryPublic, tags=[Tags.industries], summary="Get an industry by id")
async def get_industry(industry_id: int, session: SessionDep):
    """Retrieve an industry information by its ID:

    - **industry_id**: The ID of the industry to retrieve.
    """
    industry = session.get(Industry, industry_id)

    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")

    return industry


@app.patch('/industries/{industry_id}', response_model=IndustryPublic, tags=[Tags.industries], summary="Update an industry by id")
async def update_industry(industry_id: int, industry: IndustryBase, session: SessionDep):
    """Change name information about current industry:

    - **name**: each industry must have name (required)
    """
    industry_db = session.get(Industry, industry_id)

    if not industry_db:
        raise HTTPException(status_code=404, detail="Industry not found")

    industry_data = industry.model_dump(exclude_unset=True)
    industry_db.sqlmodel_update(industry_data)
    session.add(industry_db)
    session.commit()
    session.refresh(industry_db)

    return industry_db


@app.delete('/industries/{industry_id}', status_code=204, tags=[Tags.industries], summary="Delete an industry by id")
async def delete_industry(industry_id: int, session: SessionDep):
    """Delete full industry information from database by ID:

    - **industry_id**: The ID of the industry to delete.
    """
    industry = session.get(Industry, industry_id)

    if not industry:
        raise HTTPException(status_code=404, detail="Industry not found")

    session.delete(industry)
    session.commit()

    return {"ok": True}


@app.post('/numbers-of-empoyees/', status_code=201, response_model=NumberOfEmployeesPublic, tags=[Tags.number_of_employees], summary="Create a group of number of employees")
async def create_number_of_employees(number_of_employees: NumberOfEmployeesBase, session: SessionDep):
    """Create a group of numbers of employees with amount of employees value:

    - **name**: amount of employees, for example: 200-1000 (required)
    """
    db_numbers_of_emloyees = NumberOfEmployees.model_validate(
        number_of_employees)
    session.add(db_numbers_of_emloyees)
    session.commit()
    session.refresh(db_numbers_of_emloyees)

    return db_numbers_of_emloyees


@app.get('/numbers-of-employees/', tags=[Tags.number_of_employees], summary="Get all groups of number of emloyees")
async def read_number_of_employees(session: SessionDep) -> Page[NumberOfEmployeesPublic]:
    """Retrieve a paginated list of all groups of number of employees. You can choose page and how many groups of number of employees will be displayed in each page"""
    numbers_of_employees = session.exec(select(NumberOfEmployees)).all()

    return paginate(numbers_of_employees)


@app.get('/numbers-of-employees/{number_id}', response_model=NumberOfEmployeesPublic, tags=[Tags.number_of_employees], summary="Get a group of number of emloyees")
async def get_number_of_employee(number_id: int, session: SessionDep):
    """Retrieve a group's of number of employees information by its ID:

    - **number_id**: The ID of the group of number of employees to retrieve.
    """
    number_of_employees = session.get(NumberOfEmployees, number_id)

    if not number_of_employees:
        raise HTTPException(
            status_code=404, detail="Number of employees not found")

    return number_of_employees


@app.patch("/number_of_employeeses/{number_id}", response_model=NumberOfEmployeesPublic, tags=[Tags.number_of_employees], summary="Update a group of number of emloyees")
def update_number_of_employees(number_id: int, number_of_employees: NumberOfEmployeesBase, session: SessionDep):
    """Change amount of employees information about current group:

     - **name**: amount of employees, for example: 200-1000  (required)
    """
    number_of_employees_db = session.get(NumberOfEmployees, number_id)

    if not number_of_employees_db:
        raise HTTPException(
            status_code=404, detail="Group of number of employees not found")

    number_of_employees_data = number_of_employees.model_dump(
        exclude_unset=True)
    number_of_employees_db.sqlmodel_update(number_of_employees_data)
    session.add(number_of_employees_db)
    session.commit()
    session.refresh(number_of_employees_db)

    return number_of_employees_db


@app.delete("/number_of_employeeses/{number_id}", status_code=204, tags=[Tags.number_of_employees], summary="Delete a group of number of emloyees")
def delete_number_of_employees(number_id: int, session: SessionDep):
    """Delete full group of number of employees information from database by ID:

    - **number_id**: The ID of the group of number of employees to delete.
    """
    number_of_employees = session.get(NumberOfEmployees, number_id)

    if not number_of_employees:
        raise HTTPException(
            status_code=404, detail="Group of number of employees not found")

    session.delete(number_of_employees)
    session.commit()

    return {"ok": True}
