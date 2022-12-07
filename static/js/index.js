document.getElementById("file").addEventListener("change", function() {
    var media = URL.createObjectURL(this.files[0]);
    var video = document.getElementById("video");
    video.src = media;
    video.style.display = "block";
    video.play();
  });

function uploadFile(form){
    const formData = new FormData(form);

    // if name of file is not set, prompt user to upload
    if(!formData.get("static_file").name) {
        alert("Please select a video to upload")
        return
    }
    var oOutput = document.getElementById("static_file_response")

    // create new post request
    var oReq = new XMLHttpRequest();
    oReq.open("POST", "upload_static_file", true);

    // handle response of python server
    oReq.onload = function(oEvent) {
        if (oReq.status == 200) {
            oOutput.innerHTML = "Uploaded!";
            resp = JSON.parse(oReq.responseText)
            console.log(resp)
            alert(resp.filename + " successfully uploaded!")

            // redirect user to get_scores server function
            // note: window.location.href uses GET, but really should
            // be using POST here...
            scores_url = "/get_scores?fn="
            scores_url += encodeURIComponent(resp.filename)
            window.location.href = scores_url;}

            // fetch("/get_scores", {
            //     method: "POST",
            //     headers: {'Content-Type': 'application/json'},
            //     body: resp,
            //     redirect: "follow",
            //   })
            //   .then((response) => response.json())
            // }
        else {
            oOutput.innerHTML = "Error occurred when trying to upload your file.<br>";
            }
        };

    // send user's file to python server
    oOutput.innerHTML = "Sending file...";
    console.log("Sending file...")
    oReq.send(formData);
}


// function send_vid_data(video_contents){

//     alert("hello")
//     if (typeof video_contents == 'undefined') {
//         alert("Please upload a video")
//         return
//     }

//     let data = {
//         "video": video_contents,
//         //"timestamp": timestamp
//     };

//     alert("about to fetch")
//     // // Handle announcement
//     fetch("/get_scores",
//         {method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify(data)})
//     .then((response) => response.text())
//     .then((text) => {
//         if (text=="success")
//             alert("Successfully sent your announcement!")
//         else alert("Error - unable to send announcement")
//     });
// }
