# Hotel Reservation Backend

Simple Flask backend for a university DevOps final project.

The backend provides the API for a hotel reservation system and connects to MongoDB.

## Technologies

- Python
- Flask
- MongoDB
- Docker
- GitHub Actions

## Project Structure

```text
backend-repo-devops-project/
├── .github/
│   └── workflows/
├── src/
│   ├── app.py
│   ├── database.py
│   └── reservation.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/` | Backend health message |
| GET | `/hotels` | Return all hotels |
| POST | `/reservation` | Create a new reservation |
| GET | `/reservation/<reservation_id>` | Get reservation by ID, full name, or email |
| DELETE | `/reservation/<reservation_id>` | Cancel reservation by ID |

## Reservation Validation

When creating a reservation, the backend validates:

- Required fields
- Hotel exists
- Check-in date is not in the past
- Check-out date is after check-in date
- Reservation dates do not overlap for the same hotel

## Environment Variables

The backend reads MongoDB configuration from environment variables:

| Variable | Description |
| --- | --- |
| `MONGO_HOST` | MongoDB service host |
| `MONGO_PORT` | MongoDB port |
| `MONGO_HOSTS` | MongoDB Replica Set hosts |
| `MONGO_REPLICA_SET` | MongoDB Replica Set name |
| `MONGO_AUTH_SOURCE` | MongoDB authentication database |
| `DATABASE_NAME` | MongoDB database name |
| `MONGO_USERNAME` | MongoDB username |
| `MONGO_PASSWORD` | MongoDB password |

## Build Docker Image

```bash
docker build -t hotel-backend:v1 .
```

## Run Docker Container

```bash
docker run -d --name hotel-backend -p 5000:5000 hotel-backend:v1
```

## CI/CD

Pipeline 1 runs on push to the `dev` branch.

It builds the Docker image and pushes it to Docker Hub:

```text
adibush/hotel-backend
```

Pipeline 2 runs after Pipeline 1 completes successfully.

It updates the backend image tag in the infrastructure repository, opens a pull request from `dev` to `main`, and merges it automatically.
