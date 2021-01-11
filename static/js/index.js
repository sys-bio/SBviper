/**
 * Name: Frank Yu
 * Date: November 20 2020
 *
 * This is the JS to implement the functions for web-based version of
 * restaurant online ordering system. It provides features that allow user to check the menu,
 * order the dishes listed on the menu, and review their order based on the phone number
 * they have left for ordering.
 * It will display proper error messages if an error occurs.
 */
"use strict";

(function() {
  let options = new Set();
  window.addEventListener("load", init);

  /**
   * sets up button's functionality when page loads
   */
  function init() {
    id("filtered-btn").addEventListener("click", function() {
      openTab('filtered-content')
    });
    id("non-filtered-btn").addEventListener("click", function() {
      openTab('non-filtered-content')
    });
    id("all-btn").addEventListener("click", function() {
      openTab('all-content')
    });
    id("input-form").addEventListener("submit", function(eve) {
      eve.preventDefault();
      runMatcher();
    });
    id("display-variables").addEventListener("change", selectToDisplay);
  }

  function selectToDisplay() {
    if (this.value === "all") {
      showAllGraphs();
    } else {
      hideAllGraphs();
      let targets = document.getElementsByClassName(this.value);
      for (let i = 0; i < targets.length; i++) {
        targets[i].style.display = "";
      }
    }
  }

  function hideAllGraphs() {
    let allImg = qsa("img");
    for (let i = 0; i < allImg.length; i++) {
      allImg[i].style.display = "none";
    }
  }

  function showAllGraphs() {
    let allImg = qsa("img");
    for (let i = 0; i < allImg.length; i++) {
      allImg[i].style.display = "";
    }
  }

  function openTab(tabId) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabId).style.display = "block";
    event.currentTarget.className += " active";
  }

  function runMatcher() {
    let params = new FormData(id("input-form"));
    fetch('/run', {method: "POST", body: params})
      .then(checkStatus)
      .then(resp => resp.json())
      .then(showResponse)
      .catch(handleError);
  }

  function showResponse(res) {
    let filtered = res.filtered;
    let non_filtered = res['non-filtered'];
    for (let i = 0; i < filtered.length; i++) {
      let imgPath = filtered[i][0];
      let img = gen("img");
      img.src = "images/filtered/" + imgPath;
      img.id = imgPath;
      img.classList.add(filtered[i][1]);
      id("filtered-content").appendChild(img);
      if (!options.has(filtered[i][1])) {
        let option = gen("option");
        option.value = filtered[i][1];
        option.text = filtered[i][1];
        options.add(filtered[i][1])
        id("display-variables").appendChild(option);
      }
    }
    for (let i = 0; i < non_filtered.length; i++) {
      let imgPath = non_filtered[i][0];
      let img = gen("img");
      img.src = "images/non_filtered/" + imgPath;
      img.id = imgPath;
      img.classList.add(non_filtered[i][1]);
      id("non-filtered-content").appendChild(img);
      if (!options.has(non_filtered[i][1])) {
        let option = gen("option");
        option.value = non_filtered[i][1];
        option.text = non_filtered[i][1];
        options.add(non_filtered[i][1])
        id("display-variables").appendChild(option);
      }
    }
    let imgPath = "all.png"
    let img = gen("img");
    img.src = "images/all/" + imgPath;
    img.id = imgPath;
    id("all-content").appendChild(img);
  }


  /**
   * This function is called when an error occurs when making request to restaurant server.
   * Displays a user-friendly error message on the page.
   * @param {Error} err - the err details of the request.
   */
  function handleError(err) {
    console.log(err);
    let response = gen("p");
    let msg = "There was an error contact the server." +
              "Please try again later.";
    if (err.message.includes(":")) {
      let indexStart = err.message.indexOf(":") + 1;
      let indexEnd = err.message.indexOf("}");
      msg += ("Error from server was " + err.message.substring(indexStart, indexEnd));
    } else {
      msg += "Error from server was: " + err.message;
    }
    response.textContent = msg;
    id("result-window").appendChild(response);
  }

  /** ------------------------------ Helper Functions  ------------------------------ */
  /**
   * Returns the element that has the ID attribute with the specified value.
   * @param {string} idName - element ID
   * @returns {object} DOM object associated with id.
   */
  function id(idName) {
    return document.getElementById(idName);
  }

  /**
   * Returns the array of elements that match the given CSS selector.
   * @param {string} selector - CSS query selector
   * @returns {object[]} array of DOM objects matching the query.
   */
  function qsa(selector) {
    return document.querySelectorAll(selector);
  }

  /**
   * Returns a new element with the given tag name.
   * @param {string} tagName - HTML tag name for new DOM element.
   * @returns {object} New DOM object for given HTML tag.
   */
  function gen(tagName) {
    return document.createElement(tagName);
  }

  /**
   * Helper function to return the response's result text if successful, otherwise
   * returns the rejected Promise result with an error status and corresponding text
   * @param {object} res - response to check for success/error
   * @return {object} - valid response if response was successful, otherwise rejected
   *                    Promise result
   */
  async function checkStatus(res) {
    if (!res.ok) {
      throw new Error(await res.text());
    }
    return res;
  }
})();