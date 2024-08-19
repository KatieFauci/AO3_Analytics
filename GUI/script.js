eel.expose(printToOutput);
function printToOutput(output) {
    console.log("IN JAVASCRIPT PRINT FUNCTION");
    ele = document.getElementById("output-box");
    console.log(ele.innerHTML);
    ele.innerHTML = ele.innerHTML + "<br>" + output;
    ele.scrollTop = ele.scrollHeight;
}

function getSearchInfo() {
  const searchTypeElement = document.querySelector('input[name="search-type"]:checked');
  const searchType = searchTypeElement ? searchTypeElement.value : null;

  const selectedRatings = Array.from(document.querySelectorAll('input[name="rating"]:checked'))
    .map(ratingInput => ratingInput.value);
  
  const wordCountSlider = document.getElementById('word-count-slider');
  const wordCount = wordCountSlider ? wordCountSlider.value : null;

  return {
    searchType,
    selectedRatings,
    wordCount
  };
}

//--------------------------------------------------
//
//  Tab Navigation
//
//--------------------------------------------------

//** Opens the Default tab */
function defaultTab(tabId){
    document.getElementById(tabId).click();
    openTab()
}

//** Opens the tab clicked */
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


//--------------------------------------------------
//
//  Button Actions
//
//--------------------------------------------------
function clickHistoryButton() { 
                  
    var doc = document.getElementById("get-history-btn");

    // get the username and password from the fields
    var user_field = document.getElementById("un").value;
    var pass_field = document.getElementById("pwd").value;

    console.log(user_field)
    console.log(pass_field)
      
    // Changing the text content
    doc.textContent = "Getting History...";

    //run scrape
    eel.get_history_clicked(user_field, pass_field);
};

async function fillUserStats() {
  // Build Table sring
  const table = await eel.fill_stats_table()();
  document.getElementById("stats-table").innerHTML = table;
};

async function searchClicked(){
  console.log("Search Initiated");
  var searchTerm = document.getElementById("search-input").value;
  var searchType = document.querySelector('input[name="search-type"]:checked').value;
  console.log(getSearchInfo())
  const table = await eel.get_search_results(searchTerm, searchType)();
  document.getElementById("search-results-table").innerHTML = table;
};


//--------------------------------------------------
//
//  Table Construction
//
//--------------------------------------------------
async function fillTagsTable(thisTable, tagClass) {
  var table = "empty table";
  console.log(table);
  if (!tagClass) {
    table = await eel.fill_tags_table()();
    console.log(table);
  }
  else{
    table = await eel.fill_tags_table(tagClass)();
  }
  document.getElementById(thisTable).innerHTML = table;
}

async function fillCharacterList() {
  // Build Table string
  const table = await eel.fill_character_list()();
  document.getElementById("user-list").innerHTML = table;
};

async function fillShipsTable() {
  const table = await eel.fill_ships_table()();
  document.getElementById("ship-table").innerHTML = table;
}


async function fillRecentlyVisitedTable() {
  const table = await eel.fill_recently_visited_table()();
  document.getElementById("recently-visited-table").innerHTML = table;
}




