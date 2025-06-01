console.log("Script loaded"); // Put this at the top of the file

function toggleDarkMode() {
    if (document.getElementById("color-sheet").getAttribute("href") === "/static/dark-colors.css") {
        document.getElementById("color-sheet").setAttribute("href", "/static/colors.css");
        document.cookie = "dark_mode=false; path=/";
        setCookie("dark_mode", "false", 999); // Set cookie
    }
    else {
        document.getElementById("color-sheet").setAttribute("href", "/static/dark-colors.css");
        setCookie("dark_mode", "true", 999); // Set cookie
    }

}



function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

const darkMode = getCookie("dark_mode");
console.log("Dark mode cookie value: " + darkMode);

const colorSheet = document.getElementById("color-sheet");
if (!colorSheet) {
    console.warn("Element with ID 'color-sheet' not found.");
}

if (darkMode === "true") {
    colorSheet.setAttribute("href", "/static/dark-colors.css");
} else if (darkMode === "false") {
    colorSheet.setAttribute("href", "/static/colors.css");
}