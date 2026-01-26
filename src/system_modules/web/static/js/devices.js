// Device class to represent a device
class Device {
  constructor(id, name, status, ip, ports) {
    this.id = id;
    this.name = name;
    this.status = status;
    this.ip = ip;
    //this.ports = ports;
  }
}

function populateDeviceTable(devices) {
  const table = document.getElementById("deviceTable");
  //table.innerHTML = ''; // Clear existing rows

  devices.forEach((device) => {
    const row = document.createElement("div");
    row.className = "table-item";
    if (device.status === "Offline") {
      row.classList.add("disabled");
    }

    // Create table cells
    const checkboxCell = document.createElement("div");
    checkboxCell.className = "table-cell";
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkboxCell.appendChild(checkbox);

    const nameCell = document.createElement("div");
    nameCell.className = "table-cell";
    nameCell.textContent = device.name;

    const statusCell = document.createElement("div");
    statusCell.className = "table-cell";
    if (device.status === "Online") {
      statusCell.classList.add("enabled");
    } else if (device.status === "Offline") {
      statusCell.classList.add("disabled");
    }
    statusCell.textContent = device.status;

    const ipCell = document.createElement("div");
    ipCell.className = "table-cell";
    ipCell.textContent = device.ip;

    const optionsCell = document.createElement("div");
    optionsCell.className = "table-cell";
    optionsCell.textContent = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"; // Placeholder for options

    // Append cells to the row
    row.appendChild(checkboxCell);
    row.appendChild(nameCell);
    row.appendChild(statusCell);
    row.appendChild(ipCell);
    row.appendChild(optionsCell);

    // Append row to the table
    table.appendChild(row);
  });
}

// Populate the table on page load
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(async function () {
    peers = await window.request_server_data("get", "database", "peers");
    devices = [];
    peers.data.peers.forEach((element) => {
      devices.push(
        new Device(
          element.device_id,
          element.device_name,
          "Online",
          element.device_ip,
          element.device_port
        )
      );
    });
    populateDeviceTable(devices);
  }, 500);
});
