import Table from "../../components/Table";
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import CreateContent from "../Content/CreateContent";

export default function Content() {
    return (
    <>
      <div className='main_content'>
        <Routes>
            <Route index element={<ContentTable />} />
            <Route path="create" element={<CreateContent />} />
        </Routes>
      </div>
    </>
  )
}

function ContentTable() {
    const data = [
        {
            name: "Vid Test",
            type: "Video",
            active: "False",
        },
        {
            name: "Slide Test",
            type: "Slideshow",
            active: "False",
        },
        {
            name: "Page Test",
            type: "Web Page",
            active: "True",
        },
        ];


    const columns = [
        { key: "name", label: "Name" },
        { key: "type", label: "Type" },
        { key: "active", label: "Is Active?" },
    ];

    return (
      <div className="dashboard_card">
        <NavLink to={"create"} className={`block hover:bg-(--color-background-accent) bg-(--color-surface) p-2 pb-1 pt-1 rounded w-fit border border-gray-700 `}>Create</NavLink>
        <hr></hr>
        <Table data={data} columns={columns} />
      </div>
    )
}