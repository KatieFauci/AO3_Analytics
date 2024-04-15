eel.expose(printToOutput);
function printToOutput(output) {
    console.log("IN JAVASCRIPT PRINT FUNCTION");
    ele = document.getElementById("output-box");
    console.log(ele.innerHTML);
    ele.innerHTML = ele.innerHTML + "<br>" + output;
    ele.scrollTop = ele.scrollHeight;
}

function defaultTab(){
    document.getElementById("defaultOpen").click();
}

function defaultTagTab(){
  document.getElementById("Tags").getElementById("defaultTagTab").click();
}

function openTab(evt, tabName, parentTabId) {
  console.log("openTab called with tabName:", tabName, "and parentTabId:", parentTabId);  
  var i, tabcontent, tablinks;

  // Get all tab content elements within the parent tab
  tabcontent = document.getElementById(parentTabId).querySelectorAll(".tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all tab link elements within the parent tab
  tablinks = document.getElementById(parentTabId).getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab
  document.getElementById(tabName).style.display = "block";

  // Add "active" class to the clicked button
  evt.currentTarget.className += " active";
}
