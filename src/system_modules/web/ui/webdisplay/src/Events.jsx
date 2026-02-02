import Table from "./components/Table"

export default function Events() {
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
    <>
      <div className='main_content'>
          <div className="dashboard_card">
            <Table data={data} columns={columns} />
          </div>
      </div>
    </>
  )
}