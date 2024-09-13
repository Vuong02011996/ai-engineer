# TEST APIS
The test mongodb server is setup in docker. If not already running, start it by rerun the `docker-compose up` command in the root directory.
## Step 1: Change the environment to test
Change the environment to test in the `.env` file in the root directory.
```
# DATABASE TEST # TODO: Uncomment this when use the test database
MONGO_DATABASE_URI=mongodb://localhost:27018
MONGO_DATABASE=oryza-ai_db_test
```
## Step 2: Load the test data
Run the following command to load the test data into the test database.
```
mongorestore --uri="mongodb://localhost:27018" "./app/tests/mock_data"
```
## Step 3: Run the tests
Run the following command to run the tests.
```
pytest
```
If you want to run a specific test file, run the following command.
```
pytest app/tests/test_file_name.py
```
If you want to run a specific test function, run the following command.
```
pytest app/tests/test_file_name.py::test_function_name
```
Result of the tests will be displayed in the terminal.

If you want to ignore the warnings, run the command with flag:
```
pytest -p no:warnings
```

**If there is any failure, you should first check the `init_db.json` file to confirm the mock data is correct. Then, you can check the test file to see what is wrong.**