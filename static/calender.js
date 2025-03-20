const CALENDER = document.getElementById("calenderBody")

function range(start, end) {
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}


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
        return arr.slice().sort((a, b) => a.start_time - b.start_time);
    }

    sort_events_endtime(arr) {
        return arr.slice().sort((a, b) => a.end_time - b.end_time);
    }

    generate_events_html() {
        let overlapping = []
        let sorted = this.sort_events(this.events)
        // Determine Overlaps
        for (let i = 0; i < sorted.length - 1; i++) {
            for (let j = i + 1; j < sorted.length; j++) {
                if (sorted[j].start_time.getTime() < sorted[i].end_time.getTime()) {
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

        let html = ""
        // Normal Events
        for (let i = 0; i < sorted.length; i++) {
            if (all_multi_index.has(i) == false) {
                let starting_slot = this.get_slot(sorted[i].start_time)
                let ending_slot = this.get_slot(sorted[i].end_time)

                html += `<div class="event" style="background: ${sorted[i].color}; grid-row: ${starting_slot}/${ending_slot};">${sorted[i].name}</div>`
            }
        }

        // Multi Events
        for (let i = 0; i < condensed_overlap.length; i++) {
            let temp_events = []
            for (let j = 0; j < condensed_overlap[i].length; j++) {
                temp_events.push(sorted[condensed_overlap[i][j]])
            }
            let sorted_temp_events = this.sort_events(temp_events)
            let starting_slot = this.get_slot(sorted_temp_events[0].start_time)
            let ending_slot = this.get_slot(this.sort_events_endtime(sorted_temp_events)[sorted_temp_events.length - 1].end_time)
            let temp = ""
            let filled_slots = [[]]

            for (let j = 0; j < sorted_temp_events.length; j++) {
                let event_starting_slot = this.get_slot(sorted_temp_events[j].start_time) - starting_slot
                let event_ending_slot = this.get_slot(sorted_temp_events[j].end_time) - starting_slot
                let column = -1;
                for (let coll = 0; coll < filled_slots.length; coll++) {
                    if (filled_slots[coll].includes(event_starting_slot) == false) {
                        column = coll;
                        break;
                    }
                }
                if (column == -1) {
                    filled_slots.push([])
                    column = filled_slots.length - 1
                }
                filled_slots[column] = filled_slots[column].concat(range(event_starting_slot, event_ending_slot - 1))

                temp += `<div class="event" style="background: ${sorted_temp_events[j].color}; grid-row: ${event_starting_slot + 1}/${event_ending_slot + 1}; grid-column: ${column + 1};">${sorted_temp_events[j].name}</div>`
            }
            temp = `<div class="multi-event" style="grid-row: ${starting_slot}/${ending_slot}; grid-template-rows: repeat(${ending_slot - starting_slot}, 1fr); grid-template-columns: repeat(${filled_slots.length}, 1fr);">` + temp
            temp += "</div>"
            html += temp
        }
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
        return (hours - this.starting_hour) * 4 + Math.floor(min / 15) + 1
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