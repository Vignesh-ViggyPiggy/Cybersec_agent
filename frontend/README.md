# CyberSec Agent Frontend

Modern React-based web interface for the CyberSec Agent log analysis system.

## Features

- 🎨 Modern, dark-themed UI
- 📝 Large text area for log input
- 🚀 Real-time analysis with loading indicators
- 📊 Structured result display with severity indicators
- 🎯 Visual representation of confidence scores
- 📱 Responsive design
- ⚡ Quick sample logs for testing
- 🔍 API health status monitoring

## Installation

```bash
cd frontend

# Install dependencies
npm install
```

## Development

```bash
# Start development server (runs on http://localhost:3000)
npm run dev
```

The frontend will automatically proxy API requests to `http://localhost:8080`.

## Build for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
```

## Usage

1. **Start the Backend API** (in separate terminal):
   ```bash
   cd ..
   python -m src.api.server
   ```

2. **Start the Frontend**:
   ```bash
   npm run dev
   ```

3. **Open Browser**:
   Navigate to `http://localhost:3000`

4. **Analyze Logs**:
   - Enter log text in the input area
   - Click quick sample buttons for examples
   - Toggle Brave Search option as needed
   - Click "Analyze Log" or press Ctrl+Enter

## Configuration

Create `.env` file in frontend directory to customize:

```env
VITE_API_URL=http://localhost:8080
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── LogInput.jsx      # Log input component
│   │   └── ResultViewer.jsx  # Results display component
│   ├── api.js                 # API client functions
│   ├── App.jsx                # Main app component
│   ├── App.css                # App styles
│   ├── index.css              # Global styles
│   └── main.jsx               # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Features Breakdown

### Log Input
- Multi-line text area with character counter
- Quick sample buttons for common attack patterns
- Option to enable/disable Brave Search
- Keyboard shortcut (Ctrl+Enter) for quick analysis

### Result Viewer
- Color-coded severity badges (CRITICAL, HIGH, MEDIUM, LOW, INFO)
- Confidence score with visual progress bar
- Detailed explanation section
- Indicators of Compromise (IOCs) list
- Recommended actions list
- Collapsible raw analysis view
- Loading state with spinner
- Error handling with user-friendly messages

### API Integration
- Health check on startup
- Automatic reconnection handling
- Error message display
- Loading states

## Keyboard Shortcuts

- `Ctrl + Enter`: Analyze log
- `Escape`: Clear focus (browser default)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Troubleshooting

### Cannot connect to API
Ensure the backend API is running:
```bash
cd ..
python -m src.api.server
```

### Port 3000 already in use
Change the port in `vite.config.js`:
```javascript
server: {
  port: 3001  // Use different port
}
```

### CORS issues
The backend API already has CORS enabled for all origins. If you still face issues, check your browser console for specific error messages.
