'use strict';

var video = document.querySelector('#video');
// var canvas = document.querySelector('#canvas');
// var context = canvas.getContext('2d');
var constraints = {
  audio: false,
  video: true
};

navigator.mediaDevices.getUserMedia(constraints)
.then(function(mediaStream) {
  video.srcObject = mediaStream;
  video.onloadedmetadata = function(e) {
    video.play();
  };
})
.catch(function(err) {
  console.log(err.name + ": " + err.message);
});

// document.querySelector('#startbutton').addEventListener('click', function() {
// //   context.drawImage(video, 0, 0, 640, 480);
//   var dataURL = canvas.toDataURL();
//   $.ajax({
//     type: "POST",
//     url: "/video_feed",
//     data: dataURL,
//     success: function(response) {
//       console.log(response);
//     }
//   });
// });