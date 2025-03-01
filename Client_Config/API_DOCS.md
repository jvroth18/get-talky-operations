# Get Talky Frontend UI API Documentation

This document describes the UI APIs available for the Get Talky frontend application.

## Request Objects API

### Get Request Objects

Retrieves application requests for a client with optional status filtering.

**Endpoint:** `GET /api/ui/get_request_objects`

**Query Parameters:**
- `client_id` (required): UUID of the client
- `status` (optional): Filter by status ("pending", "approved", or "declined")

**Example Request:**
```bash
GET /api/ui/get_request_objects?client_id=550e8400-e29b-41d4-a716-446655440000&status=pending
```

**Response:**
```json
[
  {
    "id": 1,
    "request_type": "General Consultation",
    "appointment_length": 30,
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "pet_type": "Dog",
    "pet_name": "Buddy",
    "pet_age": 3,
    "pet_sex": "Male",
    "provider_name": "Dr. Jane Smith",
    "appointment_date": "2023-06-15T14:30:00",
    "status": "pending",
    "call_summary": "Initial consultation about pet health concerns"
  }
]
```

## Client Interactions API

### Get Client Interactions

Retrieves all interactions for a client.

**Endpoint:** `GET /api/ui/get_client_interactions`

**Query Parameters:**
- `client_id` (required): UUID of the client

**Example Request:**
```bash
GET /api/ui/get_client_interactions?client_id=550e8400-e29b-41d4-a716-446655440000
```

**Response:**
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "start_time": "2023-06-15T14:30:00",
    "end_time": "2023-06-15T15:00:00",
    "phone_number": "+1234567890",
    "call_summary": "Initial consultation about pet health concerns"
  }
]
```

## Request Status Update API

### Update Request Status

Updates the status of a request.

**Endpoint:** `PUT /api/ui/update_request_status`

**Request Body:**
```json
{
  "request_id": 123,
  "status": "approved"  // "pending", "approved", or "declined"
}
```

**Response:**
```json
{
  "id": 123,
  "request_status_id": 2,
  "request_type_id": 1,
  "provider_id": 3,
  "request_time": "2023-06-15T14:30:00"
}
```

## Example Usage

### JavaScript/Fetch Implementation

```javascript
// Function to get request objects
async function getRequestObjects(clientId, status = null) {
  let url = `http://your-server.com/api/ui/get_request_objects?client_id=${clientId}`;
  if (status) {
    url += `&status=${status}`;
  }
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return await response.json();
}

// Function to get client interactions
async function getClientInteractions(clientId) {
  const url = `http://your-server.com/api/ui/get_client_interactions?client_id=${clientId}`;
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json'
    }
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return await response.json();
}

// Function to update request status
async function updateRequestStatus(requestId, status) {
  const response = await fetch('http://your-server.com/api/ui/update_request_status', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      request_id: requestId,
      status: status
    })
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return await response.json();
}
```

## Setup Instructions

Before using these APIs, make sure to initialize the request status enum values by running:

```bash
python init_enums.py
```

This will create the necessary status values (pending, approved, declined) in the database. 