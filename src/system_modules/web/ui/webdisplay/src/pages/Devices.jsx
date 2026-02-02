import { useState } from 'react'
import Table from '../components/Table';
export default function Devices() {
    return (
    <>
      <div className='main_content'>
          <DeviceTable />
      </div>
    </>
  )
}

function DeviceTable() {
    const data = [
        {
            id: "pi-01",
            name: "Raspberry Pi",
            status: "online",
            ip: "192.168.1.10",
            cpu: 42,
        },
        {
            id: "cam-02",
            name: "Camera",
            status: "offline",
            ip: "192.168.1.24",
            cpu: null,
        },
        ];


    const columns = [
        { key: "name", label: "Device" },
        { key: "ip", label: "IP Address" },
        {
            key: "status",
            label: "Status",
            render: (value) => (
            <span
                className={
                value === "online"
                    ? "text-green-400"
                    : "text-red-400"
                }
            >
                {value}
            </span>
            ),
        },
        {
            key: "cpu",
            label: "CPU",
            render: (value) =>
            value !== null ? `${value}%` : "—",
        },
    ];

    return (
    <div className="dashboard_card overflow-x-auto">
      <Table columns={columns} data={data} />
    </div>
  );
}