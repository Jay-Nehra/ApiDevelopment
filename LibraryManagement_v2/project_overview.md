### Library Management V2

In this project, I'm building on the original library management system, continuing with the books API but refining it to make the `books` object more robust.

> The new API will be more sophisticated than the initial version. Alongside the basic `GET`, `POST`, `PUT`, and `DELETE` methods, I'll be handling data validation, custom exceptions, specific status codes, API documentation with Swagger, and adding logging and configuration. I’ll also work with Python request objects.

I'll start by creating a new `Book` class to work directly with Python objects.

---

### CRUD Operations

I’m revisiting CRUD operations to reinforce key concepts:

| CRUD Operation | HTTP Request Method |
|----------------|---------------------|
| Create         | POST                |
| Read           | GET                 |
| Update         | PUT                 |
| Delete         | DELETE              |

---

### Project Setup

1. **Create Project Structure**: Start with a new project folder and set up a `books2.py` script, where I’ll define the `Book` class and initialize the `BOOKS` object.
   
2. **Data Validation**: An issue I faced previously was with unvalidated data, like users entering a non-numeric ID or a rating above 5. So, this time I'll ensure data is validated before creating new books.
   - **Solution**: Use Pydantic for data validation, which allows for data modeling and error handling right in the data model.
   
3. **Request Model with Pydantic**: I’ll create a request model for validating incoming data, using Pydantic’s syntax, which is very similar to standard Python class syntax.
   
4. **Object Conversion**: After validation, I’ll convert the Pydantic request object to a Python `Book` object.
   
5. **Add to Collection**: Once validated and converted, I’ll add the new book to the `BOOKS` list.
   
6. **Status Codes and Exception Handling**: I’ll handle both standard and custom exceptions and manage response codes.

---

### HTTP Status Codes

Understanding status codes is critical:

- **1xx Informational**: Request received, process continues.
- **2xx Success**: Indicates successful processing.
   - **200 OK**: General success (often used for `GET`).
   - **201 Created**: Resource created (for `POST`).
   - **204 No Content**: Success, but no content to return (for `PUT`, `DELETE`).
- **4xx Client Error**: Issues on the client's side.
   - **400 Bad Request**: Invalid request.
   - **401 Unauthorized**: Authentication needed.
   - **403 Forbidden**: Access denied.
   - **404 Not Found**: Resource not found.
   - **422 Unprocessable Entity**: Semantic errors in request data.
- **5xx Server Error**: Issues on the server side.
   - **500 Internal Server Error**: Unexpected server error.

---

### API Development Checklist

Here’s my step-by-step guide for API development with FastAPI:

1. **Define API Purpose**  
   - Clarify the API’s goals (e.g., CRUD for book data with rating filters).

2. **Identify Key Models and Data Structures**  
   - Define essential models (`Book`, `BookRequest`). I’ll keep separate models for requests and responses to manage validation effectively.

3. **Implement Validation with Pydantic**  
   - Set field constraints (e.g., `min_length`, `gt`, `lt`) to validate data inputs.

4. **Define Endpoints (URLs and Methods)**  
   - Ensure each endpoint uses the right HTTP method and has clear, descriptive paths (e.g., `/books/{book_id}`, `/books/filter`).

5. **Plan Routing Logic and Parameters**  
   - Avoid path conflicts (e.g., `/books` vs. `/books/filter`) and decide when to use path vs. query parameters.

6. **Data Persistence Strategy**  
   - Decide if data will be in-memory (e.g., list) or in a database and manage unique identifiers for each item.

7. **Logging**  
   - Log all significant actions with a consistent format for better debugging (e.g., `info` for normal actions, `error` for failures).

8. **Handle Success and Error Responses**  
   - Confirm actions (e.g., “Book created”) and use appropriate error codes (`404` for not found, `400` for bad requests).

---

### Next Steps

**Testing and Debugging**
   - **Unit Testing**: Write unit tests for all endpoints, covering edge cases.
   - **Manual Testing**: Use Postman or FastAPI’s docs to test each scenario and confirm responses are correct. 

---
