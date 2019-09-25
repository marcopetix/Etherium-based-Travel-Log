
var targets = [];
var targets_names = [];
var users = [];
var markers = [];
var markers_progress = [];
var subMarkers = [];

function get_targets() {
  targets = [];
  targets_name = [];
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {

  if (this.readyState == 4 && this.status == 200) {
    var myJSON = JSON.parse(this.responseText);
    for( x in myJSON["data"]){
      targets.push({'lat': parseFloat(myJSON["data"][x][2]), "lng": parseFloat(myJSON["data"][x][3])});
      targets_names.push(myJSON["data"][x][1]);
      }
    //console.log(targets);
    }
  };

  xhttp.open("GET", "http://127.0.0.1:5000/targets", true);
  xhttp.send();
}

function get_users() {
  users = [];
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var myJSON = JSON.parse(this.responseText);
    for(x in myJSON["data"]){
      users.push(myJSON["data"][x]);
      var y = parseInt(x) + 1;
      document.getElementById("users").innerHTML += '<button class="btn" onclick="get_markers(' + "'" + users[x] + "'" +  ')">Utente ' + y + '</button>     ';
    }
    //console.log(users)
    change_color();
    }
  };
  xhttp.open("GET", "http://127.0.0.1:5000/users", true);
  xhttp.send();
}

function get_markers(address) {
  markers = [];
  markers_progress = [];
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    var myJSON = JSON.parse(this.responseText);
    //console.log(myJSON);

    for( x in myJSON["data"]){
      markers.push({'lat': parseFloat(myJSON["data"][x][2]), "lng": parseFloat(myJSON["data"][x][3])});
      markers_progress.push({'description': myJSON['data'][x][1], 'progress':myJSON['data'][x][4], 'status':myJSON['data'][x][5]});
      }
    //console.log(markers);
    initMap();
    }
  };

  xhttp.open("GET", "http://127.0.0.1:5000/user_markers/" + address, true);
  xhttp.send();
}

function change_color(){
  var header = document.getElementById("users");
  var btns = header.getElementsByClassName("btn");
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
    var current = document.getElementsByClassName("active");
    if (current.length > 0) {
      current[0].className = current[0].className.replace(" active", "");
    }
    this.className += " active";
    });
  }
}

function status_color(progress, status){
  if(progress == "START")
    return "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png";
  if (progress == "TRAVELLING")
      return "http://maps.google.com/mapfiles/ms/icons/red-dot.png";
  if (status == "TRUE" && progress == "END")
      return "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
  if (status == "FALSE" && progress == "END")
      return "http://maps.google.com/mapfiles/ms/icons/purple-dot.png";
}

function initMap() {
  var subMarkers = [];
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 15, center: targets[0]});
  for(x in targets){
    addMarker(targets[x], map, "http://maps.google.com/mapfiles/ms/icons/blue-dot.png", targets_names[x]);
  }
  for(x in markers){
    addMarker(markers[x], map, status_color(markers_progress[x]['progress'], markers_progress[x]['status']), markers_progress[x]['description']);
  }

  for (x in markers){
    subMarkers.push(markers[x]);

    if( markers_progress[x]['progress'] == "END" ){

    addPolyline(subMarkers, map);
    subMarkers = [];
    }

  }
  if(subMarkers != []){
    addPolyline(subMarkers, map);
    subMarkers = [];
  }

}

function checkEnd(marker, map) {
  return marker['progress'] == "END";
}

function addPolyline(markers, map) {
  var path = new google.maps.Polyline({
    path: markers,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2
    });

    path.setMap(map);
}

function addMarker(location, map, color, title) {
  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: title,
    icon: {
      url:color
    }
  });
}
