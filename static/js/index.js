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
    var upload_status = document.getElementById("upload status")
    var analyze_status = document.getElementById("analyze status")

    // create new post request
    var oReq = new XMLHttpRequest();
    oReq.open("POST", "upload_static_file", true);

    // handle response of python server
    oReq.onload = function(oEvent) {
        if (oReq.status == 200) {
            upload_status.innerHTML = "Video uploaded!";
            resp = JSON.parse(oReq.responseText)
            console.log(resp)
            // alert(resp.filename + " successfully uploaded!")

            // redirect user to get_scores server function
            // note: window.location.href uses GET, but really should
            // be using POST here...
            timestamp = document.getElementById("video").currentTime
            score_url = "/get_scores?fn="
            score_url += encodeURIComponent(resp.filename)
            score_url += "&timestamp="
            score_url += encodeURIComponent(timestamp)
            analyze_status.innerHTML = "Analyzing video..."
            window.location.href = score_url;}

            // fetch("/get_scores", {
            //     method: "POST",
            //     headers: {'Content-Type': 'application/json'},
            //     body: resp,
            //     redirect: "follow",
            //   })
            //   .then((response) => response.json())
            // }
        else {
            upload_status.innerHTML = "Error occurred when trying to upload your file.<br>";
            }
        };

    // send user's file to python server
    upload_status.innerHTML = "Sending file...";
    console.log("Sending file...")
    oReq.send(formData);
}