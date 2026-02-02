import Table from "./components/Table"

export default function Content() {
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
    <>
      <div className='main_content'>
          <div className="dashboard_card">
            <Table data={data} columns={columns} />
          </div>
      </div>
    </>
  )
}