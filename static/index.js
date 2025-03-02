

var createElement = (function () {

    return function (tagName, attributes) {
        attributes = attributes || {};
        var element = document.createElement(tagName);
        for (var attr in attributes) {
            if (attributes.hasOwnProperty(attr)) {
                element.setAttribute(attr, attributes[attr]);
            }
        }
        return element;
    };

})();








document.getElementById("presentationType").onchange = updatePresentationFields;

function updatePresentationFields() {
    selector = document.getElementById("presentationType");
    if (selector.value == "publishedSlide" || selector.value == "viewingSlide") {
        let elements = document.getElementsByClassName("form-slides-options")

        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "block";
        };
        elements = document.getElementsByClassName("form-url-options")
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        };
        elements = document.getElementsByClassName("form-idle-options")
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        };
    }
    else if (selector.value == "idle") {
        let elements = document.getElementsByClassName("form-slides-options")
        updatePreviewURL(null);
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        };
        elements = document.getElementsByClassName("form-url-options")
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        };
        elements = document.getElementsByClassName("form-idle-options")
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "block";
        };
    }
    else {
        let elements = document.getElementsByClassName("form-slides-options")

        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        };
        elements = document.getElementsByClassName("form-url-options")
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "block";
        };
        elements = document.getElementsByClassName("form-idle-options")
        for (let i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        };
    }
}

function settingsClear() {
    let elements = document.getElementsByClassName("controls")

    for (let i = 0; i < elements.length; i++) {
        elements[i].style.display = "none";
    };
}

function refreshImage(img) {
    const currentSrc = img.src.split("?")[0];  // Remove existing query params
    img.src = currentSrc + "?t=" + new Date().getTime();  // Add a unique timestamp
}




//Canvas section
const canvas = document.getElementById("previewCanvas");
const ctx = canvas.getContext("2d");
var width = 1200;
var height = 600;
canvas.width = width
canvas.height = height
// ctx.fillStyle = "red";
// ctx.fillRect(0, 0, width, height / 2)
// ctx.fillStyle = "blue";
// ctx.fillRect(0, height / 2, width, height/2)
canvasLeft = canvas.offsetLeft + canvas.clientLeft,
    canvasTop = canvas.offsetTop + canvas.clientTop,
    daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


ctx.font = "30px Arial";
ctx.fillStyle = "white";
ctx.fillText("AM", ((width - 200) / 4) + 200 - 20, 30)
ctx.fillText("PM", ((width - 200) / 4) * 3 + 200 - 20, 30)
ctx.strokeStyle = "lightgrey"
ctx.lineWidth = 5;
ctx.beginPath(); // Start a new path
ctx.moveTo(200 + 5, 35); // Move the pen to (30, 50)
ctx.lineTo(200 + ((width - 200) / 2) - 5, 35); // Draw a line to (150, 100)
ctx.stroke(); // Render the path
ctx.beginPath(); // Start a new path
ctx.moveTo(200 + ((width - 200) / 2) + 5, 35); // Move the pen to (30, 50)
ctx.lineTo(width - 5, 35); // Draw a line to (150, 100)
ctx.stroke(); // Render the path
tickDist = (width - 200) / 24
for (let j = 1; j < 24; j++) {
    ctx.strokeStyle = "rgb(100 100 100)"
    ctx.lineWidth = 2;
    ctx.beginPath(); // Start a new path
    ctx.moveTo(200 + (tickDist * j), (height / 8) * 1 - 20); // Move the pen to (30, 50)
    ctx.lineTo(200 + (tickDist * j), (height / 8) * 7 + 20); // Draw a line to (150, 100)
    ctx.stroke(); // Render the path
    if (true) {
        ctx.font = "20px Arial";
        ctx.fillStyle = "white";
        if (j <= 12) {
            ctx.fillText(j, 200 + (tickDist * j) - 7, (height / 8) * 7 + 40)
        }
        else {
            ctx.fillText((j - 12), 200 + (tickDist * j) - 7, (height / 8) * 7 + 40)
        }
        // if (j >= 23) {
        //     ctx.fillText((12), 200 + (tickDist * 0) - 7, (height / 8) * 7 + 40)
        // }
    }
}

for (let i = 1; i <= daysOfWeek.length; i++) {
    ctx.font = "30px Arial";
    ctx.fillStyle = "white";
    ctx.fillText(daysOfWeek[i - 1], 10, (height / 8) * i + 10)

    ctx.lineWidth = 2;
    ctx.strokeStyle = "rgb(43 43 43)";
    ctx.strokeRect(200, (height / 8) * i - 10, width - 200, 20)



}

let events = []

function displayEvent(id, day, color, startTime, endTime, type, name, data) {
    let index = daysOfWeek.indexOf(day) + 1;

    ctx.fillStyle = color;
    ctx.fillRect(200 + tickDist * startTime, (height / 8) * index - 10, tickDist * (endTime - startTime), 20)
    events.push({
        "wkDay": day,
        "id": id,
        "color": color,
        "startTime": startTime,
        "endTime": endTime,
        "name": name,
        "type": type,
        "data": data
    })
}

function sendEventToServer(id, name, color, wkDay, startTime, endTime, type, data) {
    let serverData = {
        "name": name,
        "color": color,
        "wkDay": wkDay,
        "startTime": startTime,
        "endTime": endTime,
        "type": type,
        "data": data,
        "id": id
    }
    fetch("/api/add/schedule/event/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(serverData)
    })
        .then(response => {
            if (response.ok) {
                // Successful submission, reload the page
                window.location.reload();
            } else {
                response.json().then(data => {
                    alert("Form submission failed: " + data.code);
                })

            }
        })
        .catch(error => console.error("Error:", error));
}
canvas.addEventListener('click', function (event) {
    var { x, y } = getCanvasCoordinates(event)
    events.forEach(element => {

        let index = daysOfWeek.indexOf(element.wkDay) + 1;
        let ymin = (height / 8) * index - 10
        let ymax = (height / 8) * index + 10
        let xmin = 200 + tickDist * element.startTime
        let xmax = 200 + tickDist * element.endTime
        if (ymax >= y && y >= ymin && xmax >= x && x >= xmin) {
            loadEvent(element)
        }
    });
}, false);

function convertHoursToHHMM(hours) {
    let hh = Math.floor(hours);
    let mm = Math.round((hours % 1) * 60);
    return `${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}`;
}


function loadEvent(event) {
    form.getElementsByTagName("select")[0].value = event.type
    document.getElementById("identifier").value = event.id
    let type = event.type
    let peerSelect = document.getElementById("peerSelect")
    let elements = peerSelect.getElementsByTagName("input")
    for (let i = 0; i < elements.length; i++) {
        elements[i].checked = false
        for (let j = 0; j < event.data.peers.length; j++) {
            if (elements[i].name == event.data.peers[j]) {
                elements[i].checked = true
            }
        }
    };


    if (type == "publishedSlide" || type == "viewingSlide") {
        let section = form.querySelector(".form-slides-options")
        section.querySelector("#url").value = event.data.url
        section.querySelector("#startTime").value = convertHoursToHHMM(event.startTime)
        section.querySelector("#name").value = event.name
        section.querySelector("#endTime").value = convertHoursToHHMM(event.endTime)
        section.querySelector("#color").value = event.color
        section.querySelector("#restart").checked = event.data.restart
        section.querySelector("#start").checked = event.data.autoStart
        section.querySelector("#delay").value = event.data.delay
        section.querySelector("#wkDay").value = event.wkDay
    }
    else if (type == "URL") {
        let section = form.querySelector(".form-url-options")
        section.querySelector("#url").value = event.data.url
        section.querySelector("#startTime").value = convertHoursToHHMM(event.startTime)
        section.querySelector("#name").value = event.name
        section.querySelector("#endTime").value = convertHoursToHHMM(event.endTime)
        section.querySelector("#color").value = event.color
        section.querySelector("#wkDay").value = event.wkDay
    }
    else if (type == "idle") {
        let section = form.querySelector(".form-idle-options")
        section.querySelector("#startTime").value = convertHoursToHHMM(event.startTime)
        section.querySelector("#name").value = event.name
        section.querySelector("#endTime").value = convertHoursToHHMM(event.endTime)
        section.querySelector("#color").value = event.color
        section.querySelector("#wkDay").value = event.wkDay
    }
    updatePresentationFields()
}



function getCanvasCoordinates(event) {
    const rect = canvas.getBoundingClientRect(); // Get canvas position and size relative to the viewport
    const scaleX = canvas.width / rect.width;    // Horizontal scale ratio
    const scaleY = canvas.height / rect.height;  // Vertical scale ratio

    // Convert page coordinates (event.clientX/Y) to canvas coordinates
    const x = (event.clientX - rect.left) * scaleX;
    const y = (event.clientY - rect.top) * scaleY;

    return { x, y };
}

const form = document.getElementById('presentation');

function deleteEvent(id) {
    fetch("/api/remove/schedule/event/" + id).then(response => {
        if (response.ok) {
            // Successful submission, reload the page
            window.location.reload();
        }
    })
        .catch(error => console.error("Error:", error));
}


function processEvent(newEvent) {
    let id = newEvent ? "0" : document.getElementById("identifier").value
    let type = form.getElementsByTagName("select")[0].value;
    let peers = []

    let peerSelect = document.getElementById("peerSelect")
    let elements = peerSelect.getElementsByTagName("input")
    for (let i = 0; i < elements.length; i++) {
        if (elements[i].checked) {
            peers.push(elements[i].name)
        }
    };


    if (type == "publishedSlide" || type == "viewingSlide") {
        let section = form.querySelector(".form-slides-options")
        let url = section.querySelector("#url").value
        let startTime = section.querySelector("#startTime").value
        startTime = parseInt(startTime.split(":")[0]) + parseInt(startTime.split(":")[1]) / 60
        let name = section.querySelector("#name").value
        let endTime = section.querySelector("#endTime").value
        endTime = parseInt(endTime.split(":")[0]) + parseInt(endTime.split(":")[1]) / 60
        let color = section.querySelector("#color").value
        let restart = section.querySelector("#restart").checked
        let start = section.querySelector("#start").checked
        let delay = section.querySelector("#delay").value
        let wkDay = section.querySelector("#wkDay").value
        displayEvent(id, wkDay, color, startTime, endTime, type, name, {
            "url": url,
            "restart": restart,
            "autoStart": start,
            "delay": delay,
            "peers": peers
        })
        sendEventToServer(id, name, color, wkDay, startTime, endTime, type, {
            "url": url,
            "restart": restart,
            "autoStart": start,
            "delay": delay,
            "peers": peers
        })
    }
    else if (type == "URL") {
        let section = form.querySelector(".form-url-options")
        let url = section.querySelector("#url").value
        let startTime = section.querySelector("#startTime").value
        startTime = parseInt(startTime.split(":")[0]) + parseInt(startTime.split(":")[1]) / 60
        let name = section.querySelector("#name").value
        let endTime = section.querySelector("#endTime").value
        endTime = parseInt(endTime.split(":")[0]) + parseInt(endTime.split(":")[1]) / 60
        let color = section.querySelector("#color").value
        let wkDay = section.querySelector("#wkDay").value
        displayEvent(id, wkDay, color, startTime, endTime, type, name, {
            "url": url,
            "peers": peers
        })
        sendEventToServer(id, name, color, wkDay, startTime, endTime, type, {
            "url": url,
            "peers": peers
        })
    }
    else if (type == "idle") {
        let section = form.querySelector(".form-idle-options")
        let startTime = section.querySelector("#startTime").value
        startTime = parseInt(startTime.split(":")[0]) + parseInt(startTime.split(":")[1]) / 60
        let name = section.querySelector("#name").value
        let endTime = section.querySelector("#endTime").value
        endTime = parseInt(endTime.split(":")[0]) + parseInt(endTime.split(":")[1]) / 60
        let color = section.querySelector("#color").value
        let wkDay = section.querySelector("#wkDay").value
        displayEvent(id, wkDay, color, startTime, endTime, type, name, {
            "peers": peers
        })
        sendEventToServer(id, name, color, wkDay, startTime, endTime, type, {
            "peers": peers
        })
    }
};


// <option value="publishedSlide">Published - Google Slides</option>
// <option value="viewingSlide">Anyone can view - Google Slides</option>
// <option value="URL">URL</option>
// <option value="idle">Idle Screen</option>


fetch("./api/get/schedule/event/")
    .then((response) => response.json())
    .then((json) => {
        json.forEach(element => {
            displayEvent(element.id, element.wk_day, element.color, element.start_time, element.end_time, element.type, element.name, JSON.parse(element.data))
        });

    });


function updatePreviewURL(url) {
    let type = form.getElementsByTagName("select")[0].value;
    if (type == "publishedSlide") {
        document.getElementById("previewIframe").src = "https://docs.google.com/presentation/d/e/" + url.split("/")[url.split("/").length - 2] + "/embed";
    }
    else if (type == "viewingSlide") {
        document.getElementById("previewIframe").src = "https://docs.google.com/presentation/d/" + url.split("/")[url.split("/").length - 2] + "/view";
    }
    else if (type == "URL") {
        document.getElementById("previewIframe").src = url
    }
    else if (type == "idle") {
        document.getElementById("previewIframe").src = "/idle"
    }
}

function setdisabled(id, state) {
    if (state) {
        fetch("/api/disable/peer/" + id)
    }
    else {
        fetch("/api/enable/peer/" + id)
    }
}

function addPeer(event) {
    event.preventDefault();
    let serverData = {
        "ip": document.getElementById("addPeerIP").value,
        "port": document.getElementById("addPeerPort").value
    }
    fetch("/api/add/peer/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(serverData)
    })
        .then(response => {
            if (response.ok) {
                // Successful submission, reload the page
                window.location.reload();
            } else {
                response.json().then(data => {
                    alert("Form submission failed: " + data.code);
                })

            }
        })
        .catch(error => console.error("Error:", error));
}