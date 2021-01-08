/**
 * Name: Frank Yu
 * Date: November 20 2020
 * Section: CSE 154 AA Tal Wolman
 *
 * This is the JS to implement the functions for web-based version of
 * restaurant online ordering system. It provides features that allow user to check the menu,
 * order the dishes listed on the menu, and review their order based on the phone number
 * they have left for ordering.
 * It will display proper error messages if an error occurs.
 */
"use strict";

(function() {

  window.addEventListener("load", init);

  /**
   * sets up button's functionality when page loads
   */
  function init() {
    id("input-form").addEventListener("submit", function(eve) {
      eve.preventDefault();
      submitRequest();
    });
    id("menu-btn").addEventListener("click", checkMenu);
    id("log-dishes").addEventListener("click", reviewOrder);
  }

  /**
   * Place an order based on the name, phone number, dish, and notes inputs
   * Display messages whether the order is sucessfully placed.
   */
  function submitRequest() {
    let params = new FormData(id("input-form"));
    fetch('/orderDish', {method: "POST", body: params})
      .then(checkStatus)
      .then(resp => resp.text())
      .then(showResponse)
      .catch(handleError);
  }

  /**
   * Review the orders have been placed based on the phone number input
   * Display all the dishes ordered by the phone number
   * Display error messages if failed.
   */
  function reviewOrder() {
    let phoneNumber = id("phone-order-input").value;
    fetch('/reviewOrder?phone=' + phoneNumber)
      .then(checkStatus)
      .then(resp => resp.json())
      .then(displayOrders)
      .catch(handleError);
  }

  /**
   * Display the meanu on the page
   * Display error messages if failed.
   */
  function checkMenu() {
    fetch('/menu')
      .then(checkStatus)
      .then(resp => resp.json())
      .then(displayMenu)
      .catch(handleError);
  }

  /**
   * Display the response message of whether the order is sucessfully placed.
   * @param {string} res - String object of the response message
   */
  function showResponse(res) {
    let response = gen("p");
    response.textContent += res;
    id("result-window").appendChild(response);
  }

  /**
   * Display the orders that contained in the res.
   * @param {object} res - Json object of the orders
   */
  function displayOrders(res) {
    let response = gen("p");
    let orders = 'You have ordered ';
    for (let i = 0; i < res.length; i++) {
      orders += res[i].dish + " ";
    }
    response.textContent += orders;
    id("result-window").appendChild(response);
  }

  /**
   * Clear out the old menu that already displayed on the page.
   * Display the new menu that contained in the res.
   * @param {object} res - Json object of the menu
   */
  function displayMenu(res) {
    let food = res.MENU;
    let oldMenu = qsa("#menu-window p");

    // clean the old view of the menu
    for (let i = 0; i < oldMenu.length; i++) {
      oldMenu[i].remove();
    }

    // add the new view of the menu
    for (let i = 0; i < food.length; i++) {
      let foodName = gen("p");
      foodName.textContent = food[i];
      id("menu-window").appendChild(foodName);
    }
  }

  /**
   * This function is called when an error occurs when making request to restaurant server.
   * Displays a user-friendly error message on the page.
   * @param {Error} err - the err details of the request.
   */
  function handleError(err) {
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