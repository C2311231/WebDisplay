import { useState } from 'react'

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
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-left">
        <thead className="text-gray-400 border-b border-gray-700">
          <tr>
            {columns.map(col => (
              <th key={col.key} className="px-3 py-2">
                {col.label}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map(row => (
            <tr
              key={row.id}
              className="border-b border-gray-800 hover:bg-gray-800/50"
            >
              {columns.map(col => (
                <td key={col.key} className="px-3 py-2">
                  {col.render
                    ? col.render(row[col.key], row)
                    : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}