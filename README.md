[![Build Status - GitHub](https://github.com/YaPeL/faststore-api/workflows/test/badge.svg)](https://github.com/YaPeL/faststore-api/actions?query=workflow%3Atest)
[![](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/downloads/release/python-3710/)

<pre>


 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || |      __      | || |    _______   | || |  _________   | || |    _______   | || |  _________   | || |     ____     | || |  _______     | || |  _________   | || |              | || |      __      | || |   ______     | || |     _____    | |
| | |_   ___  |  | || |     /  \     | || |   /  ___  |  | || | |  _   _  |  | || |   /  ___  |  | || | |  _   _  |  | || |   .'    `.   | || | |_   __ \    | || | |_   ___  |  | || |              | || |     /  \     | || |  |_   __ \   | || |    |_   _|   | |
| |   | |_  \_|  | || |    / /\ \    | || |  |  (__ \_|  | || | |_/ | | \_|  | || |  |  (__ \_|  | || | |_/ | | \_|  | || |  /  .--.  \  | || |   | |__) |   | || |   | |_  \_|  | || |    ______    | || |    / /\ \    | || |    | |__) |  | || |      | |     | |
| |   |  _|      | || |   / ____ \   | || |   '.___`-.   | || |     | |      | || |   '.___`-.   | || |     | |      | || |  | |    | |  | || |   |  __ /    | || |   |  _|  _   | || |   |______|   | || |   / ____ \   | || |    |  ___/   | || |      | |     | |
| |  _| |_       | || | _/ /    \ \_ | || |  |`\____) |  | || |    _| |_     | || |  |`\____) |  | || |    _| |_     | || |  \  `--'  /  | || |  _| |  \ \_  | || |  _| |___/ |  | || |              | || | _/ /    \ \_ | || |   _| |_      | || |     _| |_    | |
| | |_____|      | || ||____|  |____|| || |  |_______.'  | || |   |_____|    | || |  |_______.'  | || |   |_____|    | || |   `.____.'   | || | |____| |___| | || | |_________|  | || |              | || ||____|  |____|| || |  |_____|     | || |    |_____|   | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 


</pre>

## Running the code


You should have docker and docker compose installed.

To start you development environment just run :

```sh
  docker-compose build
  docker-compose up
```

Or if you want to run the container in detached mode:

```sh
  docker-compose up -d
```

To stop it:

```sh
  docker-compose down
```

## docs
visit http://localhost:8000/docs#/

## Running the tests

make sure you have 2 env variables env: test and SQLALCHEMY_DATABASE_URL: "postgresql://postgres:postgres@localhost/db"
set, otherwise the tests are more of a proof of concept than real tests, as I didn't have enough time to set up postgress on github actions
```sh
  python3 -m venv/
  source env/bin/activate
  pip install -r test-requirements.txt
  pytest app/tests
```
## Details
The project comprises two main tables: Products and Inventory.
It provides a basic CRUD (Create, Read, Update, Delete) functionality for products,
along with two additional methods for listing and grouping.

The first method allows you to retrieve all products, sorted either by title or creation date.
The second method focuses on grouping products by category or tag. 
It generates a list of products associated with each category/tag, including their respective titles and IDs.

The second table, dedicated to inventory management, Currently provides basic functionality,
but it has the potential to evolve into a more comprehensive stock management system in the future.

By combining the CRUD operations for products, along with the listing, grouping, and inventory management features, this project facilitates the organization, tracking, and potential expansion of your product inventory effectively.

## Why Fast Api?

I chose FastAPI to challenge myself and make the project more engaging, even though, I have very little experience with it.

## TO-DO
- Implement migrations (I didn't include them initially for simplicity).
- Implement cursor-based pagination.
- Split the models file into separate files.
- Increase test coverage and add more tests.
- add a coverage bag to the project :)