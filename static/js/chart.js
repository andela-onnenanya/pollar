
//var appUrl = window.location.origin;

$(document).ready(function(){
  google.charts.load('current', {packages: ['bar', 'corechart', 'table']});
  
  google.charts.setOnLoadCallback(loadChart);
  
  function loadChart(){
    $.ajax({
      type: "GET",
      url: `${appUrl}/api${urlPath}`,
      success: drawChart
    });
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

});

var chartOptions = {
  'width':650,
  'chartArea':{width:'70%',height:'70%', left:"25%", top: 50},
  'backgroundColor' : {fill: '#F2F3F4'},
  'colors':['#512E5F','#F5B041', '#641E16', '#F39C12', '#C39BD3', '#17202A', '#0B5345'],
  'height':400};


function drawChart(response){
  const votes = response.votes
  const message = response.message
  if (votes.length == 0){
    document.getElementById('chart').innerHTML = "<div rel='no-chart'>This poll has no votes yet. Be the first to vote!</div>"
  }
  else{
    var chart = new google.visualization.PieChart(document.getElementById('chart'));
    document.getElementById('chart').innerHTML = "";
    var data = new google.visualization.DataTable();    
    data.addColumn('string', 'Name');
    data.addColumn('number', 'Votes');
     
     // Set chart options
    var len = votes.length;
    while (len){
      var vote = votes[len-1];
      data.addRow([vote.name, vote.vote]);
      len--
    }
    chart.draw(data, chartOptions);
  }
}
