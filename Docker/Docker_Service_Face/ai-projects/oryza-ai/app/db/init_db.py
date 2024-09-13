import argparse

from app.schemas.company_schemas import CompanyCreate
from app.schemas.user_schemas import UserCreate
from app.services.company_services import company_services
from app.services.user_services import user_services

# Create the parser
parser = argparse.ArgumentParser(description="Initialize the database with some data")

# Add the arguments
parser.add_argument("--email", type=str, help="The email of the superuser")
parser.add_argument("--username", type=str, help="The username of the superuser")
parser.add_argument("--password", type=str, help="The password of the superuser")

# Parse the arguments
args = parser.parse_args()


def init_db() -> None:
    # Create Oryza company if not exists
    company_exists = company_services.get_company_by_name(name="Oryza")
    if company_exists:
        company = company_exists
    else:
        company_create = CompanyCreate(name="Oryza", domain="oryza.com")
        company = company_services.create_company(obj_in=company_create)
    # Get superuser info
    if args.email and args.password:
        email = args.email
        password = args.password
        if args.username:
            username = args.username
        else:
            username = email.split("@")[0]

        print(company)

        # Create superuser
        user_in = UserCreate(
            email=email,
            username=username,
            password=password,
            company_id=str(company.id),
            is_superuser=True,
            is_active=True,
        )
        user = user_services.create_user(obj_in=user_in, is_active=True)
    print("User created")
    print("User info:", user)


init_db()
