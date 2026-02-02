import { useState } from 'react'
import { LineChart, Line, Pie, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, PieChart } from 'recharts';
import Table from '../components/Table.jsx'


export default function Dashboard() {
    const data = [
        {
            id: "pi-01",
            name: "Raspberry Pi",
            status: "online",
            ip: "192.168.1.10",
            cpu: 42,
            fill: "#4ade80"
        },
        {
            id: "cam-02",
            name: "Camera",
            status: "offline",
            ip: "192.168.1.24",
            cpu: 5,
            fill: "#f87171"
        },
        ];


    const cpuData = [
        { time: '10:00', cpu: 12 },
        { time: '10:01', cpu: 18 },
        { time: '10:02', cpu: 25 },
    ];
    
    return (
    <>
      <div className='main_content grid lg:grid-cols-5 sm:grid-cols-1 md:grid-cols-3 gap-5 row'>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <DeviceStateCard data={data}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <AlertsCard />
          <CpuGraph data={cpuData} />
      </div>
    </>
  )
}

export function CpuUsageCard({ usage }) {
  return (
    <div className="dashboard_card">
      <div className="flex justify-between items-center mb-2">
        <h3>CPU Usage</h3>
        <span className="text-sm font-semibold text-gray-100">
          {usage}%
        </span>
      </div>
       <hr></hr>
      <div className="w-full h-2 bg-gray-700 rounded overflow-hidden">
        <div
          className="h-full bg-green-500 transition-all duration-300"
          style={{ width: `${usage}%` }}
        />
      </div>
    </div>
  );
}

function CpuGraph({data}) {
  return (
    <div className="dashboard_card">
        <h3>CPU Usage</h3>
        <hr></hr>
        <ResponsiveContainer width="100%" height="90%">
          <LineChart data={data}>
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="cpu" stroke="#8884d8" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
    </div>
  );
}

function DeviceStateCard({data}) {
  return (
    <div className="dashboard_card">
        <h3 className="">Device Status</h3>
        <hr className=''></hr>
        <ResponsiveContainer width="100%" height="100%">
            <PieChart >
            <Pie
                data={data}
                dataKey="cpu"
                nameKey="name"
                cx="50%"
                cy="40%"
                label>
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

function AlertsCard({}) {

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
        <div className="dashboard_card col-span-2">
            <h3>Alerts:</h3>
            <hr></hr>
            <Table data={data} columns={columns} />
      </div>
    )
}