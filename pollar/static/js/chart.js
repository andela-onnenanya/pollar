
//var appUrl = window.location.origin;

(function () {
  var globalResult;
  
  google.charts.setOnLoadCallback(loadChart);
  google.charts.setOnLoadCallback(updateChart);
  
  //set the semi-global variables here
  var pollID = "";
  var pollClick = "";
  var globalCurrentPoll = "";
  var globalData;

  var chartOptions = {
        'width':650,
        'chartArea':{width:'70%',height:'70%', left:"25%", top: 50},
        'backgroundColor' : {fill: '#F2F3F4'},
        'colors':['#512E5F','#F5B041', '#641E16', '#F39C12', '#C39BD3', '#17202A', '#0B5345'],
        'height':400};

  //draw chart if there are vote, else display a message
  function conditionalDraw(counter, data, options){
    // Instantiate and draw the chart.    
    var chart = new google.visualization.PieChart(document.getElementById('chart'));
    if (counter === 0){
      document.getElementById('chart').innerHTML = "<div rel='no-chart'>This poll has no votes yet. Be the first to vote!</div>"
    }
    else{
      document.getElementById('chart').innerHTML = "";
    chart.draw(data, options);
    }
  }

  function loadChart(){
    var result = globalResult;
    if(result === "[]" || result === undefined){
      document.getElementById("poll-list").innerHTML = '<li class="poll-ref">Wao! No Polls here! Please Create One.</li>';
    }else{
      var data = new google.visualization.DataTable();
      data.addColumn('string', 'Name');
      data.addColumn('number', 'Votes');
      
        // Set chart options
      var options = chartOptions;
      var voteCounter = 0;
          
      while (len){
        var currentOption = voteOptions[len-1];
        data.addRow([currentOption.name, currentOption.vote]);
        optionHtml += '<option class="vote-option" value=' + currentOption._id + '>' + currentOption.name + '</option>';
        
        //check for polls with votes other than 0;
        if(currentOption.vote > 0){ voteCounter++; }
        len--;
      }
      
      conditionalDraw(voteCounter, data, options);
    }
  }
    
  //check if user can vote for a poll
  function voterCheck(){
    var sessionVOtes = JSON.parse(sessionStorage.getItem("userVotes"));
    var len = sessionVOtes.length || 0;
    while (len){
      var vote = sessionVOtes[len-1];
      if(vote.pollName === globalCurrentPoll){
        return false;
      }
      len--;
    }
    return true;
  }
    
  //show link box
  function showLink(){
      document.getElementById("mask").style.display = "block";
      document.getElementById("linkBox").style.display = "block";
      var pollID = document.getElementsByClassName("poll-ref active")[0].getAttribute("id");
      document.getElementById("linkBoxLink").innerHTML = appUrl + "/username/polls/" + pollID;
  }

  //close link box
  function closeLink(){
      document.getElementById("mask").style.display = "none";
      document.getElementById("linkBox").style.display = "none";
  }

  function updateChart(){
    return
    // call endpoint for the submit
    // from the result, check if vote user can vote again
    // if yes, draw chart with new result,
    // else, alert user that he can not vote again
  }

  function openPoll(){
    var poll = this.getAttribute("poll");  
    
    var pollObj= JSON.parse(poll, reviver);
    document.getElementsByClassName("poll-ref active")[0].className = "poll-ref";
    this.className += " active";
    
    var voteOptions = pollObj.options,
        len = voteOptions.length;
    
    //reset current pollID
    pollID = pollObj._id;
    
    //update poll options in <select>
    var optionHtml = '<option value="" disabled selected hidden>Select Whom to vote for...</option>';
    while (len){
        var currentOption = voteOptions[len-1];      
        optionHtml += '<option class="vote-option" value=' + currentOption._id + '>' + currentOption.name + '</option>';
        len--;
      }
    
    var title = pollObj.name.length > 20? pollObj.name.slice(0, 18) + "..." : pollObj.name;
    document.getElementById("pollViewHead").innerHTML = title + ' :<span> by ' + pollObj.author + '</span>';
    document.getElementById("pollViewDesc").innerHTML = pollObj.description;
    document.getElementById("chartTitle").innerHTML = title + ' : Pie Chart.';
    document.getElementById("pollSelection").innerHTML = optionHtml;
    //update chart with updateChart function above
    updateChart(JSON.stringify(pollObj)); 
  }

  function sendVote(){
    var value = document.getElementById("pollSelection").value;
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
        var voteObj = {pollName: globalCurrentPoll},
            oldSessionVotes = JSON.parse(sessionStorage.getItem("userVotes"));
        oldSessionVotes.push(voteObj);
        sessionStorage.setItem("userVotes", JSON.stringify(oldSessionVotes))
        ajaxFunctions.ajaxRequest('POST', appUrl + "/api/votes?voteid=" + value, updateChart)
      }
    }
  }

  var submitVote = document.getElementById("submitVote");

  submitVote.addEventListener('click', sendVote, false);

  ajaxFunctions.ready(ajaxFunctions.ajaxRequest('GET', appUrl + "/api/polls-array", loadPolls));

})();

  

