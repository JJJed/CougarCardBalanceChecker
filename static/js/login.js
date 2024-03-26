function formSubmitted() {
    var message = document.getElementById("message");
    if (message == null) {
        var loading_text = document.createElement("p");
        loading_text.id = "loading_text";
        loading_text.style.color = "#ccc";
        loading_text.style.textAlign = "center";
        loading_text.textContent = "Loading...";
        var form = document.getElementById("form");
        form.appendChild(loading_text);
    } else {
        message.style.textAlign = "center";
        message.style.color = "#ccc";
        message.textContent = "Loading...";
    }
}