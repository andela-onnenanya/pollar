
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

  function addActionToClass (klass, action){
    //add click event to each of the polls in the pane
      for (var i=0; i<klass.length; i++){
        var pollClass = klass[i];
        pollClass.addEventListener('click', action, false);
      }
  }

  pollClick = document.getElementsByClassName("poll-ref")

  if (pollClick){
    addActionToClass(pollClick, openPoll)
  }

  function sendVote(){
    var choice = document.getElementById("pollSelection").value;
    if (choice){
      document.getElementById("displayBox").innerHTML = "Submitting vote . . .";
      document.getElementById("mask").style.display = "block";
      document.getElementById("displayBox").style.display = "block";
      $.ajax({
        type: "POST",
        url: `${appUrl}/api${urlPath}`,
        data: { choice },
        success: function(data){
          displayMessage(data.message);
          drawChart(data);
        }
      });
    }
  }

  
function displayMessage(message){
  document.getElementById("mask").style.display = "block";
  document.getElementById("displayBox").innerHTML = message
  document.getElementById("displayBox").style.display = "block";
  setTimeout(function(){
    document.getElementById("mask").style.display = "none";
    document.getElementById("displayBox").style.display = "none";
  }, 3000)
}
