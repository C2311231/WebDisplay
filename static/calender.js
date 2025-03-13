const CALENDER = document.getElementById("calenderBody")
class day {
    constructor(name, date) {
        this.name = name
        this.date = date
        CALENDER.innerHTML += '<div class="cal_day" data-name="' + name + `">
                <div class="cal_day_title">`  + this.name + " - " + this.date + '</div><div class="cal_day_body"></div></div>'

        let days = document.getElementsByClassName("cal_day")
        for(let i = 0; i < days.length; i++){
            if (days[i].dataset.name == this.name){
                this.html = days[i]
                return
            }
        }
    }
    add_event(name, start_time, end_time) {
        this.html.getElementsByClassName("cal_day_body")[0].innerHTML += '<div class="cal_event"><div class="cal_event_name">' + name + `
        </div><div class="cal_event_time">
                            ` + start_time + ' - '  + end_time + ` 
                        </div>
        `
    }
}