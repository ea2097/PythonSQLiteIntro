# Flight Management Database Manager

A console-based SQLite database management system for airline operations. This application provides a comprehensive interface for airline staff to manage flights, pilots, and airport information through an intuitive menu-driven system.

## Features

### Flight Management

- View real-time flight dashboards
- Track in-progress and scheduled flights
- Monitor flights with missing information
- View top 10 longest flights
- Custom flight data filtering

### Pilot Management

- View pilot assignments and schedules
- Track pilot qualifications and contact information
- Monitor pilot availability
- Custom pilot data filtering

### Airport Operations

- View airport statistics and flight counts
- Monitor scheduled flights by airport
- Track airport details and timezone information
- Custom airport data filtering

### Data Management

- Add new records to any table
- Update existing records with data validation
- Delete records with confirmation
- View data using custom filtering criteria

## Getting Started

1. Ensure Python 3.x is installed on your system
2. Clone this repository to your local machine
3. Navigate to the project directory
4. No additional `requirements.txt` needed more than python's core packages.
4. Run the application:
   ```bash
   python main.py
   ```

## Execution Workflow

1. **Main Menu Navigation**

   - View Dashboards
   - View Data by Criteria
   - Add Records
   - Edit Records
   - Delete Records

2. **Dashboard Views**

   - Flights Dashboards
   - Pilots Dashboards
   - Airports Dashboards

3. **Data Operations**
   - Select tables/views
   - Apply filters and criteria
   - Perform CRUD operations
   - View formatted results

## Database Structure

The application uses SQLite with a robust schema including:

- Flight information and schedules
- Pilot details and assignments
- Airport information and statistics
- Custom views for efficient data retrieval

## Features for Airline Staff

- **Flight Management**

  - Add and schedule new flights
  - Update flight status and details
  - View flights by various criteria
  - Track flight durations and status

- **Pilot Operations**

  - Assign pilots to flights
  - View pilot schedules
  - Update pilot information
  - Monitor pilot assignments

- **Airport Management**
  - View destination information
  - Update airport details
  - Track flights by airport
  - Monitor airport operations

## Notes

- The application includes data validation and error handling
- Foreign key constraints are enabled for data integrity
- The interface provides clear navigation and confirmation prompts
- All operations are performed through an intuitive menu system
