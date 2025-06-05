# Frontend for AI-Driven Adaptive Learning System

This directory contains the React frontend for the system, built using Vite and styled with Tailwind CSS.

## Development Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    If you haven't already, or if dependencies have changed:
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    This will typically start the frontend application on `http://localhost:5173` (or another port if 5173 is busy). The application uses a proxy to forward API requests starting with `/api/` to the backend server (expected to be running on `http://localhost:5000`).

## Building for Production

To create a production build:
```bash
npm run build
```
This will generate static assets in the `dist` folder.

## Project Structure

-   `src/components/`: Contains reusable React components (e.g., `EyeTrackingForm.jsx`).
-   `src/App.jsx`: The main application component that sets up routing and layout.
-   `src/index.css`: Contains Tailwind CSS directives and any global styles.
-   `tailwind.config.js`: Configuration for Tailwind CSS.
-   `vite.config.js`: Configuration for Vite, including the development server proxy.
