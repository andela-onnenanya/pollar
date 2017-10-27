var appUrl = window.location.origin;
var urlPath = window.location.pathname

function openPoll(e){
  var id = e.currentTarget.id;
  window.location = `/polls/${id}`
}

function trimString(word, number){
  if (word) {
    var word = word.length > number? word.slice(0, 18) + "..." : word;
    return word;
  }else{
    return 'Chart Title'
  }
}



function addEventToClass (klass){
  //add click event to each of the polls in the pane
    for (var i=0; i<klass.length; i++){
      var pollClass = klass[i];
      pollClass.addEventListener('click', openPoll, false);
    }
}

pollClick = document.getElementsByClassName("poll-ref")

if (pollClick){
  addEventToClass(pollClick)
}

function updateChart(data){
  console.log(data)
}

function voterCheck(){
  console.log(urlPath)
  var choice = document.getElementById("pollSelection").value;
  $.ajax({
    type: "POST",
    url: `${appUrl}/api${urlPath}`,
    data: { choice },
    success: updateChart
  });
  // ajaxFunctions.ajaxRequest('POST', `${appUrl}/api${urlPath}?choice=${choice}`, updateChart)
}

function sendVote(){
  var value = document.getElementById("pollSelection").value;
  var quury = `choice=${value}`
  if(!voterCheck()){
    document.getElementById("mask").style.display = "block";
    document.getElementById("displayBox").innerHTML = "Sorry! You have already voted! You can't vote twice!";
    document.getElementById("displayBox").style.display = "block";
    setTimeout(function(){
    document.getElementById("mask").style.display = "none";
    document.getElementById("displayBox").innerHTML = "Submitting vote . . .";
    document.getElementById("displayBox").style.display = "none";
    }, 3000);
  }else{
      if (value){
        //lock the screen first
        document.getElementById("mask").style.display = "block";
        document.getElementById("displayBox").style.display = "block";
        ajaxFunctions.ajaxRequest('POST', appUrl + "/api/polls/vote?" + value, updateChart)
      }
  }
}