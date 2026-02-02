import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard.jsx'
import Devices from './pages/Devices.jsx'
import Logs from './pages/Logs.jsx';
import Content from './pages/Content.jsx';
import Events from './pages/Events/Events.jsx';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  function toggleSideBar() {
    setSidebarOpen(!sidebarOpen)
  }

  return (
    <>
    <Router>
    <div className='h-screen flex flex-col bg-gray-100'>
      <Header toggleSideBar={toggleSideBar} />
      <MainContent sidebarOpen={sidebarOpen} />
    </div>
    </Router>
    </>
  )
}

export default App


function Header({toggleSideBar}) {
  return (
    <>
      <header className="flex w-full bg-gray-600 p-3 justify-between pl-5 pr-5">

        <div className="flex gap-3">
          <button onClick={toggleSideBar}>
            <svg viewBox="0 0 24 24" aria-hidden="true" className='w-6'>
              <rect x="3" y="4" width="18" height="3" rx="1" fill="currentColor"/>
              <rect x="3" y="10.5" width="18" height="3" rx="1" fill="currentColor"/>
              <rect x="3" y="17" width="18" height="3" rx="1" fill="currentColor"/>
            </svg>
          </button>

          <h1 className=''>WebDisplay</h1>
        </div>
        <div className="flex gap-3">
            Center
        </div>
        <div className="flex gap-3">
            Right
        </div>
      </header>
    </>
  )
}

function MainContent({sidebarOpen}) {
    return (
    <>
      <main className='flex h-full'>
        <SideBar isOpen={sidebarOpen} />
        <Routes>
            <Route path="/*" element={<Dashboard />} />
            <Route path="/devices/*" element={<Devices />} />
            <Route path="/logs/*" element={<Logs />} />
            <Route path="/content/*" element={<Content />} />
            <Route path="/events/*" element={<Events />} />
        </Routes>
      </main>
    </>
  )
}

function SideBar({isOpen}) {
  return (
    <>
      <nav className={`max-w-96 h-full bg-gray-500 transition-all duration-300
        ${isOpen ? 'w-64 p-2' : 'w-0 p-0 overflow-hidden'}
      `}>
        <NavButton btn_name={"Dashboard"} url={"/"} />
        <NavButton btn_name={"Devices"} url={"/devices"} />
        <NavButton btn_name={"Content"} url={"/content"} />
        <NavButton btn_name={"Events"} url={"/events"} />
        <NavButton btn_name={"Logs"} url={"/logs"} />
      </nav>
    </>
  )
}

function NavButton({btn_name, url, icon, isOpen }) {
    return (
    <>
      <NavLink to={url} className={({ isActive }) => `block hover:bg-gray-700 p-2 m-1 rounded ${isActive ? 'bg-gray-700' : ''}`}>{btn_name}</NavLink>
    </>
  )
}