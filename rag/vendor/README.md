# Run and Up Langfuse Server Using Docker Compose

- First Clone the Langfuse Repository

To start the Langfuse server using Docker Compose, run one of the following commands:

```bash
docker compose up
# or
docker compose up -d
```

**Process Overview**

When you run this command, Docker Compose sets up and starts the Langfuse server. Here's a breakdown of the process:

1. **Image Pulling:** Docker pulls necessary images for the database (db) and Langfuse server.

2. **Infrastructure Setup:** Docker creates the required network, volumes, and containers.

3. **Database Initialization:** The PostgreSQL database is initialized and started.

4. **Database Migration:** Langfuse server applies numerous database migrations (269 total) to set up the schema and data structure.

5. **Migration Completion:** Server confirms successful application of all migrations.

6. **Optional Migrations:** If `CLICKHOUSE_URL` is not configured, related migrations are skipped.

7. **Frontend Startup:** Next.js (version 14.2.15) starts, indicating Langfuse uses Next.js for its frontend.

8. **Server Accessibility:** The server becomes accessible at [http://127.0.0.1:3000/](http://127.0.0.1:3000/) on the Docker network.

9. **Initialization Complete:** The process finishes, and the server is ready after 2.9 seconds.

**Result**

Upon successful completion, the Langfuse server is fully set up with an initialized database and all necessary migrations applied. The server is now running and ready to handle requests @ [http://127.0.0.1:3000/][http://127.0.0.1:3000/].

