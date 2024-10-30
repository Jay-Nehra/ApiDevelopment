# ApiDevelopment

This repository consolidates several API projects, each designed to address specific functionalities and use cases. Each project has its own documentation and follows best practices for API design, including data validation, custom exceptions, and status code handling.

## Projects

### 1. LibraryManagement_v1
- **Overview**: A foundational API for managing a library's book inventory.
- **Features**:
  - Basic CRUD operations for book entries.
  - Initial setup for handling data storage and retrieval.
- **Documentation**: Detailed API docs are available in the `docs` folder for `LibraryManagement_v1`.

### 2. LibraryManagement_v2
- **Overview**: An enhanced version of the Library Management API, focusing on robust data handling and extended API functionalities.
- **Features**:
  - Data validation using Pydantic.
  - Custom exception handling and detailed status codes.
  - Updated API endpoints with additional filtering options.
- **Documentation**: Detailed API docs are available in the `docs` folder for `LibraryManagement_v2`.

Additional projects will be added to this repository as development progresses, each with its own set of features and focus areas.

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Jay-Nehra/ApiDevelopment.git
   cd ApiDevelopment
   ```

2. **Set Up Virtual Environment**:
   Each project within this repository is designed to run in its own virtual environment to manage dependencies effectively.

   - For `LibraryManagement_v1`:
     ```bash
     cd LibraryManagement_v1
     pipenv install
     pipenv shell
     ```

   - For `LibraryManagement_v2`:
     ```bash
     cd LibraryManagement_v2
     pipenv install
     pipenv shell
     ```

3. **Run the API**:
   - For each project, follow its `README.md` or project-specific instructions to start the API server.

## Documentation

Comprehensive documentation for each project can be found in the respective `docs` folder. To view the HTML documentation:

1. **Build the Documentation**:
   ```bash
   cd LibraryManagement_v1/docs
   make html
   ```
   Then open `LibraryManagement_v1/docs/build/html/index.html` in your browser.

2. Repeat for `LibraryManagement_v2` or other projects.

## Contributing

Feel free to contribute by adding new features, fixing issues, or enhancing existing projects. Each project has its own structure and guidelines, so refer to individual project folders for more details.
