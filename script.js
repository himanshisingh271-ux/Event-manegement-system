const form = document.getElementById("registrationForm");

form.addEventListener("submit", function(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const phone = document.getElementById("phone").value;
    const course = document.getElementById("course").value;
    const selectEvent = document.getElementById("event").value;

    if (name === "") {
        alert("Please enter your name.");
        return;
    }

    if (phone === "") {
        alert("Please enter your phone number.");
        return;
    }

    if (course === "") {
        alert("Please enter your course.");
        return;
    }

    if (selectEvent === "") {
        alert("Please select an event.");
        return;
    }

    alert("Registration Successful!");
});
