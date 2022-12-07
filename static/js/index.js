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
