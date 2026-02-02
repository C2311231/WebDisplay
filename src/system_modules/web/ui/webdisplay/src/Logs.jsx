import Table from "./components/Table"

export default function Logs() {
    const data = [
        {
            timestamp: "10:10",
            device: "PI",
            data: "High Usage!"
        },
        {
            timestamp: "10:15",
            device: "PI 2",
            data: "Failed to start event!"
        },
        ];


    const columns = [
        { key: "timestamp", label: "Time" },
        { key: "device", label: "Device" },
        { key: "data", label: "Alert" },
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