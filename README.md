Q: 1
🎬 Movie Ticket Booking System
Goal:

Design and implement RESTful APIs for a movie ticket booking system that allows admins to manage movies, theatres, screens, and shows, and enables users to browse, select seats, and book tickets. The system should include authentication and role-based access control.

Requirements Overview
Authentication & Authorization
Implement JWT-based authentication.
Two roles:
Admin: Full access to theatre, movie, and show management.
User: Can browse and book tickets.
Protect endpoints based on roles:
Admin-only routes (prefixed with /admin) should be accessible only to admins.
User routes should be accessible only to authenticated users.
Admin Capabilities
Admins should be able to:

Create, update, and delete theatres.
Add multiple screens under each theatre.
Define seats for each screen (e.g., A1–A10, B1–B10).
Create, update, and delete movies.
Schedule shows by assigning a movie to a specific screen with date, time, and price.
View all user bookings for management and analytics.
User Capabilities
Users should be able to:

Register and log in.
View available movies and shows.
View theatre and screen details with seat layout.
Check seat availability for a selected showtime.
Select specific seats and book tickets.
View their booking history and details.
Cancel their bookings (if allowed by policy).
Schema Design
You need to design an appropriate database schema to support:

Theatres with multiple screens
Screens with defined seat structures
Shows mapped to specific screens and movies
Bookings tied to specific seats and showtimes
Role-based user management (Admin/User)
API Endpoints
Authentication
Method	Endpoint	Description
POST	/auth/register	Register a new user
POST	/auth/login	Log in and receive JWT token
Admin APIs (Protected: Admin Role Only)
Method	Endpoint	Description
POST	/admin/theatres	Create a theatre
PUT	/admin/theatres/:id	Update theatre details
DELETE	/admin/theatres/:id	Delete a theatre
POST	/admin/theatres/:id/screens	Add a screen to a theatre
PUT	/admin/screens/:id	Update screen details
DELETE	/admin/screens/:id	Delete a screen
POST	/admin/screens/:id/seats	Define seats for a screen
POST	/admin/movies	Add a new movie
PUT	/admin/movies/:id	Update movie details
DELETE	/admin/movies/:id	Delete a movie
POST	/admin/shows	Schedule a new show (movie + screen + time + price)
GET	/admin/bookings	View all user bookings
User APIs (Protected: User Role Only)
Method	Endpoint	Description
GET	/movies	Get all available movies
GET	/shows	Get list of all active shows
GET	/shows/:id	Get show details with screen and seat layout
GET	/shows/:id/seats	Get seat availability for a show
POST	/bookings	Book specific seats for a show
GET	/bookings	View user’s booking history
DELETE	/bookings/:id	Cancel a booking
Expected Deliverables
REST API implementation with role-based access control.
Proper schema design to handle theatres, screens, seats, movies, shows, and bookings.
Authentication middleware to verify JWT tokens.
Validation for booking (e.g., seat availability, double booking prevention).
Advanced Requirements
Feature	Description
Background Task	Use BackgroundTasks to send confirmation emails
Error Handling	Implement custom exceptions and global handlers
Database Design	You must design the database schema and relationships yourself for users, movies, theaters, shows, and bookings
Submission Guidelines
Submit a GitHub repository link, with a well-documented README.md with the schema diagram