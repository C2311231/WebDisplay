import Table from "../../components/Table"
import CreateEvent from "./CreateEvent"
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';


export default function Events() {
   return (
    <div className="main_content">
    <Routes>
        <Route index element={<EventTable />} />
        <Route path="create" element={<CreateEvent />} />
    </Routes>

    </div>
  )
}

function EventTable() {
    const data = [
        {
            name: "Vid Test Trigger",
            screen: "Screen 1",
            device: "Device 1",
            content: "Vid Test",
            active: "False",
        },
        {
            name: "Slide Test Trigger",
            screen: "Screen 1",
            device: "Device 1",
            content: "Slide Test",
            active: "False",
        },
        {
            name: "Page Test Trigger",
            screen: "Screen 1",
            device: "Device 1",
            content: "Page Test",
            active: "False",
        },
        ];


    const columns = [
        { key: "name", label: "Name" },
        { key: "screen", label: "Screen" },
        { key: "device", label: "Device" },
        { key: "content", label: "Content" },
        { key: "active", label: "Is Active?" },
    ];
    return (
      <div className="dashboard_card">
        <NavLink to={"create"} className={`block hover:bg-gray-700 bg-gray-900 p-2 rounded w-fit border border-gray-700 `}>Create</NavLink>
        <hr></hr>
        <Table data={data} columns={columns} />
      </div>
    )
}