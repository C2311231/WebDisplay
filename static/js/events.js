// Event class to represent a Event
class Event {
  constructor(name, groups, criteria, action, color) {
          this.name = name
          this.groups = groups
          this.criteria = criteria
          this.action = action
          this.color = color
    //this.ports = ports;
  }
}

function populateEventTable(Events) {
  const table = document.getElementById("eventTable");
  //table.innerHTML = ''; // Clear existing rows

  Events.forEach((Event) => {
    const row = document.createElement("div");
    row.className = "table-item";
    if (Event.status === "Offline") {
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
    nameCell.textContent = Event.name;

    const statusCell = document.createElement("div");
    statusCell.className = "table-cell";
    if (Event.status === "Online") {
      statusCell.classList.add("enabled");
    } else if (Event.status === "Offline") {
      statusCell.classList.add("disabled");
    }
    statusCell.textContent = Event.status;

    const ipCell = document.createElement("div");
    ipCell.className = "table-cell";
    ipCell.textContent = Event.ip;

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
    events = await window.request_server_data("get", "database", "events");
    Events = [];
    events.data.events.forEach((element) => {
      Events.push(
        new Event(
          element.name,
          element.groups,
          element.criteria,
          element.action,
          element.color
        )
      );
    });
    populateEventTable(events);
  }, 500);
});
