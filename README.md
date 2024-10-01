# PostgreSQL Database Management App

This project is a web-based application designed to manage PostgreSQL databases, allowing users to create, modify, retrieve, and delete database applications. The backend is built with the Django framework, while the frontend is powered by React. The application adheres to RESTful API conventions and follows industry standards for database management operations.

## Features

- **App Creation**: Easily create new applications in the PostgreSQL database.
- **App Modification**: Adjust the size of your applications.
- **App Information**: Retrieve detailed information about specific applications.
- **App Deletion**: Delete applications when no longer needed.
- **App Search**: List all applications with filtering options.

## Technologies Used

### Backend
- **Django**: Provides the backend structure and API endpoints.
- **PostgreSQL**: A powerful relational database system.

### Frontend
- **React**: The JavaScript library used for building a responsive and dynamic user interface.

### Additional Tools (if applicable)
- **Docker**: Containerizes the app for consistent environments and easy deployment.
- **Kubernetes**: Manage deployments across clusters for scalability and reliability.

## API Requirements & Conventions

- All endpoints begin with `/api/v1/` to denote the first version of the API.
- All endpoints receive and return JSON data.
- Proper HTTP status codes are returned:
  - `200 OK` for successful requests.
  - `201 Created` for successful resource creation.
  - `400 Bad Request` for validation errors or incorrect input.
  - `404 Not Found` if the resource does not exist.
  - `500 Internal Server Error` only if the server encounters an issue.

### API Endpoints

#### Create an App
- **Method**: POST  
- **URL**: `/api/v1/app/`
- **Request Body**:
    ```json
    {
        "name": "App Name",
        "size": 100
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "name": "App Name",
        "size": 100,
        "state": "active",
        "creation_time": "2024-10-01T12:00:00Z"
    }
    ```

#### Get a Specific App
- **Method**: GET  
- **URL**: `/api/v1/app/{app_id}/`
- **Response**:
    ```json
    {
        "id": 1,
        "name": "App Name",
        "size": 100,
        "state": "active",
        "creation_time": "2024-10-01T12:00:00Z"
    }
    ```

#### List All Apps
- **Method**: GET  
- **URL**: `/api/v1/apps/`
- **Response**:
    ```json
    {
        "results": [
            {
                "id": 1,
                "name": "App Name",
                "size": 100,
                "state": "active",
                "creation_time": "2024-10-01T12:00:00Z"
            },
            {
                "id": 2,
                "name": "Another App",
                "size": 200,
                "state": "inactive",
                "creation_time": "2024-09-30T10:30:00Z"
            }
        ]
    }
    ```

#### Update App Size
- **Method**: PUT  
- **URL**: `/api/v1/app/{app_id}/`
- **Request Body**:
    ```json
    {
        "size": 200
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "name": "App Name",
        "size": 200,
        "state": "active",
        "creation_time": "2024-10-01T12:00:00Z"
    }
    ```

#### Delete an App
- **Method**: DELETE  
- **URL**: `/api/v1/app/{app_id}/`
- **Response**:
    ```json
    {}
    ```

## Setup Instructions

### Prerequisites

Ensure you have the following software installed on your system:
- Python 3.x
- Node.js
- PostgreSQL
- Django
- React
- Docker (optional, for containerization)
- Kubernetes (optional, for cluster management)

### Backend Setup (Django)

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo/backend
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database and apply migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

### Frontend Setup (React)

1. Navigate to the frontend directory:
    ```bash
    cd ../frontend
    ```

2. Install the required dependencies:
    ```bash
    npm install
    ```

3. Start the React development server:
    ```bash
    npm start
    ```

### Docker (Optional)

If you prefer containerizing the app with Docker, follow these steps:

1. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

### Kubernetes (Optional)

To deploy the app on a Kubernetes cluster, use the provided configuration files. Ensure you have a working Kubernetes environment.

## Contributing

Feel free to fork this repository, make improvements, and submit a Pull Request. Contributions are always welcome!
