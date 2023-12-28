# Magic Post

## Project Overview

A Restful API for post delivery system.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/fastapi-project.git
   cd magic-post
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn magicpost.app:app --reload
   ```

   This will start the FastAPI application locally, and you can access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Running Tests

To run the tests, use the following command:

```bash
pytest
```

## Restore database & using PostgreSQL as production database.

> Require psql, pg_dump (included with PostgresSQL). Only tested on Linux, PostgresSQL 16.1.

1. **Connect to the database as superuser**
    ```bash
    sudo -iu postgresql psql
    ```

2. **Create database**

    ```bash
    sudo -iu postgresql createdb -T template0 magicpost_db
    ```

3. **Restore data**
    ```
    sudo -iu postgresql psql magicpost_db magicpost/data/magicpost-27-12-2023.dump
    ```

4. **Create user with permission**

    ```sql
    CREATE USER magicpost_user WITH PASSWORD 'magicpost_password';
    GRANT ALL PRIVILEGES ON DATABASE magicpost_db TO magicpost_user;
    ```

5. **Run application with database**

    ```bash
    DATABASE_URL=postgresql://magicpost_user:magicpost_password@localhost/magicpost_db uvicorn magicpost.app:app --reload
    ```

## Docker Support

Just run the dockerfile.

## API Documentation

The API documentation is generated dynamically and can be accessed at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) when the application is running.

## Contributing

Contributions are welcome!

## License

This project is licensed under the [GPL-3.0](LICENSE).

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [pytest](https://docs.pytest.org/en/stable/)