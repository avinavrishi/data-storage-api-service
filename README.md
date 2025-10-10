# JSON Storage API

A modern FastAPI application for storing and managing JSON data with update limits.

## Features

- **CRUD Operations**: Create, Read, Update, Delete JSON data
- **Update Limits**: Configurable limits on how many times each item can be updated (default: 50)
- **Timestamps**: Automatic tracking of creation and last update times
- **Pagination**: Efficient listing of stored data
- **Health Check**: Built-in health monitoring endpoint
- **Modern Architecture**: Clean separation of concerns with services, schemas, and API layers

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python run.py
   ```

3. **Access the API**:
   - API Documentation: http://127.0.0.1:8000/docs
   - Alternative docs: http://127.0.0.1:8000/redoc

## API Endpoints

### Data Management
- `POST /api/v1/data` - Create new JSON data
- `GET /api/v1/data/{item_id}` - Get JSON data by ID
- `PUT /api/v1/data/{item_id}` - Update JSON data by ID
- `DELETE /api/v1/data/{item_id}` - Delete JSON data by ID
- `GET /api/v1/data` - List all data (with pagination)

### Update Limits
- `GET /api/v1/data/{item_id}/limit-status` - Check update limit status
- `POST /api/v1/data/{item_id}/reset-counter` - Reset update counter

### Admin Endpoints
- `POST /api/v1/admin/data/{item_id}/set-max-updates` - Set max updates for a specific item

### System
- `GET /api/v1/health` - Health check

## Configuration

The application can be configured using environment variables or by modifying `app/core/config.py`:

- `DATABASE_URL`: Database connection string (default: sqlite:///./data.db)
- `API_TITLE`: API title (default: JSON Storage API)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 8000)
- `DEFAULT_MAX_UPDATES`: Default update limit (default: 50)

## Project Structure

```
app/
├── api/                    # API routes
│   └── v1/
│       ├── api.py         # API router
│       └── endpoints/     # Endpoint definitions
├── core/                  # Core functionality
│   ├── config.py         # Configuration
│   ├── database.py       # Database setup
│   └── exceptions.py     # Custom exceptions
├── schemas/              # Pydantic models
├── services/             # Business logic
└── main.py              # Application factory
```

## Example Usage

### Create Data
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/data" \
     -H "Content-Type: application/json" \
     -d '{"data": {"name": "John", "age": 30}}'
```

### Update Data
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/data/{item_id}" \
     -H "Content-Type: application/json" \
     -d '{"data": {"name": "John", "age": 31}}'
```

### Set Max Updates (Admin)
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/admin/data/{item_id}/set-max-updates" \
     -H "Content-Type: application/json" \
     -d '{"max_updates": 100}'
```

### Check Update Limit
```bash
curl "http://127.0.0.1:8000/api/v1/data/{item_id}/limit-status"
```
