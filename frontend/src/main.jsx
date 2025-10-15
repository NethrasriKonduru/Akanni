import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import akanniLogo from './assets/logo.jpg'  // <-- put your logo in src/assets/

// Dynamically set favicon
const link = document.createElement('link')
link.rel = 'icon'
link.href = akanniLogo
document.head.appendChild(link)

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)