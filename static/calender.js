const CALENDER = document.getElementById("calenderBody")

class calender {
    constructor(name, container) {
        this.name = name
        this.container = container
        this.days_container = container.getElementsByClassName("days")[0]
        this.days = []
    }

    add_day(day) {
        this.days.push(day)
        day.write(this.days_container)
    }
}

class day {
    constructor(name, date) {
        this.name = name;
        this.date = date;
        this.events = []
        this.container = null;
        this.html = null;
        this.starting_hour = 5
    }

    add_event(event) {
        this.events.push(event)
        this.generate_events_html()
    }

    sort_events(arr) {
        let n = arr.length;
        let swapped = false;
        for (let i = 0; i < n; i++) {
            swapped = false;
            for (let j = 0; j < n - i - 1; j++) {
                if (arr[j].start_time.getTime() > arr[j + 1].start_time.getTime()) {
                    [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                    swapped = true;
                }
            }

            if (swapped === false) break;
        }
        return arr;
    }

    generate_events_html() {
        let overlapping = []
        let sorted = this.sort_events(this.events)
        // Determine Overlaps
        for (let i = 0; i < sorted.length - 1; i++) {
            for (let j = i + 1; j < sorted.length; j++) {
                if (sorted[j].start_time.getTime() < sorted[i].end_time.getTime()) {
                    console.log("OVERLAP")
                    overlapping.push([i, j]); // Record overlapping pair 
                }

            }
        }
        let condensed_overlap = []
        let all_multi_index = new Set()
        for (let i = 0; i < overlapping.length; i++) {
            let found = false;
            all_multi_index.add(overlapping[i][0])
            all_multi_index.add(overlapping[i][1])
            for (let j = 0; j < condensed_overlap.length; j++) {
                if (overlapping[i][0] in condensed_overlap[j] || overlapping[i][1] in condensed_overlap[j]) {
                    found = true
                    if (overlapping[i][0] in condensed_overlap[j] == false) {
                        condensed_overlap[j].push(overlapping[i][0])
                    }
                    if (overlapping[i][1] in condensed_overlap[j] == false) {
                        condensed_overlap[j].push(overlapping[i][1])
                    }
                }
            }
            if (!found) {
                condensed_overlap.push(overlapping[i])
            }
        }
        console.log(condensed_overlap)


        let html = ""
        // Normal Events
        for (let i = 0; i < sorted.length; i++) {
            if (i in all_multi_index == false) {
                html += sorted[i].get_html()
            }
        }

        // Multi Events
        for (let i = 0; i < condensed_overlap.length; i++) {
            let temp_events = []
            for (let j = 0; j < condensed_overlap[i].length; j++) {
                temp_events.push(sorted[condensed_overlap[j]])
            }
            let sorted_temp_events = this.sort_events(temp_events)
            let starting_slot = get_slot(sorted_temp_events[0].start_time)
        }


        // Generate HTML
        // Replace Existing
        this.html.getElementsByClassName("events")[0].innerHTML = html
    }

    write(container) {
        let html = `<div class="day">
            <div class="day-header">
                <h3>${this.name}</h3>
                <p>${this.date}</p>
            </div>
            <div class="events">                
            </div>
        </div>`
        container.innerHTML += html;
        this.html = container.getElementsByClassName("day")[container.getElementsByClassName("day").length - 1];
        this.generate_events_html()
    }

    get_slot(time) {
        let hours = time.getHours()
        let min = time.getMinutes()
        return (hours - this.starting_hour) * 4 + Math.floor(min / 15)
    }
}

class event {
    constructor(name, start_time, end_time, color = "darkgrey") {
        this.name = name;
        this.start_time = start_time;
        this.end_time = end_time;
        this.color = color;
        this.date = start_time.getDate();
    }

    get_html() {
        return `<div class="event" style="background: ${this.color};">${this.name}</div>`
    }
}

let cal = new calender("test", CALENDER)

// muli-event algorithm:
// check each column for a opening in timeslot
// if no opening create new column
// if opening fill it
// if doesn't fit in rows, extend parent