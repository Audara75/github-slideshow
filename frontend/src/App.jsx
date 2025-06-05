import EyeTrackingForm from './components/EyeTrackingForm';
import './App.css'; // Keep if any global app styles are needed, or remove if empty
// Tailwind is imported in index.css, which is imported by main.jsx

function App() {
  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      {/* Added some basic page styling with Tailwind */}
      <header className="text-center mb-10">
        <h1 className="text-4xl font-bold text-indigo-700">Adaptive Learning System</h1>
        <p className="text-lg text-gray-600">Eye-Tracking Data Input</p>
      </header>
      <main>
        <EyeTrackingForm />
      </main>
      <footer className="text-center mt-10 text-sm text-gray-500">
        <p>&copy; 2024 Adaptive Learning Project</p>
      </footer>
    </div>
  );
}

export default App;
