function uploadFile(form){
    const formData = new FormData(form);
    var oOutput = document.getElementById("static_file_response")

    var oReq = new XMLHttpRequest();
    oReq.open("POST", "upload_static_file", true);
    alert(oReq)

    oReq.onload = function(oEvent) {
        if (oReq.status == 200) {
        oOutput.innerHTML = "Uploaded!";
        console.log(oReq.response)
        } else {
        oOutput.innerHTML = "Error occurred when trying to upload your file.<br \/>";
        }
        };
    oOutput.innerHTML = "Sending file!";
    console.log("Sending file!")
    oReq.send(formData);
}





let fileHandle;
let contents;
butOpenFile.addEventListener('click', async () => {
    // Destructure the one-element array.
    [fileHandle] = await window.showOpenFilePicker();
    const file = await fileHandle.getFile();
    contents = await file.text();
    textArea.value = file.size;
    });


function send_vid_data(video_contents){

    alert("hello")
    if (typeof video_contents == 'undefined') {
        alert("Please upload a video")
        return
    }

    let data = {
        "video": video_contents,
        //"timestamp": timestamp
    };

    alert("about to fetch")
    // // Handle announcement
    fetch("/get_scores",
        {method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
        if (text=="success")
            alert("Successfully sent your announcement!")
        else alert("Error - unable to send announcement")
    });
}
