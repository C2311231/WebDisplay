import { useState } from 'react'
import Table from '../components/Table';

export default function Screens() {
    return (
    <>
      <div className='main_content flex gap-4'>
          <ScreensTable />
          <ScreenGroups />
      </div>
    </>
  )
}

function ScreenGroups() {
    return (
        <div className="dashboard_card flex-1">
            <h3>Groups</h3>
            <hr></hr>
            <div className='rounded-2xl border border-(--color-text)/8 overflow-hidden'>
                <div className='p-2 text-center hover:bg-(--color-background-accent)'>Group 1</div>
                <div className='p-2 text-center hover:bg-(--color-background-accent)'>Group 2</div>
                <div className='p-2 text-center hover:bg-(--color-background-accent)'>Group 3</div>
                <div  className='p-2 text-center hover:bg-(--color-background-accent)'>Group 4</div>
                <div  className='p-2 text-center hover:bg-(--color-background-accent)'>Group 5</div>
            </div>
        </div>
    )
}


function ScreensTable() {
    const data = [
        {
            id: 1,
            name: "Raspberry Pi Screen",
            device: "Raspberry Pi",
            groups: "Group 1, Group 2",
            control: true
        },
        {
            id: 2,
            name: "Raspberry Pi Screen 2",
            device: "Raspberry Pi",
            groups: "Group 3, Group 4",
            control: false
        },
        ];


    const columns = [
        { key: "name", label: "Name" },
        { key: "device", label: "Device" },
        { key: "groups", label: "Groups" },
        {
            key: "control",
            label: "CEC Available",
            render: (value) => (
            <span
                className={
                value === true
                    ? "text-green-400"
                    : "text-red-400"
                }
            >
                {value.toString()}
            </span>
            ),
        },
    ];

    return (
    <div className="dashboard_card overflow-x-auto flex-8">
      <Table columns={columns} data={data} />
    </div>
  );
}