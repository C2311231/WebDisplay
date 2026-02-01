import { useState } from 'react'

export default function Dashboard() {
    return (
    <>
      <div className='main_content grid lg:grid-cols-5 sm:grid-cols-1 md:grid-cols-3 gap-5'>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
          <CpuUsageCard usage={50}/>
      </div>
    </>
  )
}

export function CpuUsageCard({ usage }) {
  return (
    <div className="bg-gray-800 rounded-lg p-4 shadow-md">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-sm font-medium text-gray-300">CPU Usage</h3>
        <span className="text-sm font-semibold text-gray-100">
          {usage}%
        </span>
      </div>

      <div className="w-full h-2 bg-gray-700 rounded overflow-hidden">
        <div
          className="h-full bg-green-500 transition-all duration-300"
          style={{ width: `${usage}%` }}
        />
      </div>
    </div>
  );
}
