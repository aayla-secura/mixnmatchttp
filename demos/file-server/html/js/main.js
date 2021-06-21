const api_prefix = "/api";
var debug = true;
var postLoginHooks = [];
var postLogoutHooks = [];
var page_title = null;

$(document).ready(function() {
  if (page_title === null) { page_title = document.title; }

  // Topbar
  var topbar = $('<div id="topbar"/>').prependTo("body");
  addTopbarItem('<h1 id="title"/>' , "left").text(page_title);
  addTopbarItem('<img id="menu-button" src="images/menu.svg" alt=""/>',
    "right");
  $('<div id="main"/>').prependTo("body");

  // Popups
  var menu = $('<div id="menu"/>').appendTo("body");
  addButton("Login", "login", null).appendTo(menu);
  addButton("Logout", "logout", null).appendTo(menu);
  var user = loggedInUser();
  if (! user) { $("#logout").hide(); }
  else { $("#login").hide(); }
  var input_popup = addPopup("input-popup");
  addPopupForm(input_popup, null, [], "Check", "Cancel");
  var alert_popup = addPopup("alert-popup", "");
  var login_popup = addPopup("login-popup");
  addPopupForm(login_popup, {id: "login-msg", text: "Login"},
    {
      username: {
        attrs: {
          id: "username",
          type: "text",
          placeholder: "Enter username",
        },
        props: {
          required: true,
        }
      },
      password: {
        attrs: {
          id: "password",
          type: "password",
          placeholder: "Enter password",
        },
        props: {
          required: true,
        }
      }
    }, "Login", "Close");
  $("#login-popup button.cancel").on("click", null, hideLoginPopup);

  var selector_popup = addPopup("selector-popup");
  var dropdown = $('<div class="dropdown"/>').appendTo(selector_popup);
  addButton("", null, "dropbtn").appendTo(dropdown);
  $('<div class="dropdown-content"/>').appendTo(dropdown);
  addButton("Cancel", null, "cancel").appendTo(dropdown);

  // Events
  $("#logout").click(logout);
  $("#login").click(showLoginPopup);
  $("#menu-button").click(toggleMenuPopup);
  $("#selector-popup button.dropbtn").click(function () {
    $("#selector-popup div.dropdown-content").toggle();
  });

  // Popup links
  $(".open-popup").each(function (i, el) {
    $(el).click(function () {
      var popup_id = $(this).data("popup-id");
      $("#" + popup_id).show();
    });
  })

  // Scroll to anchor
  if ($("#main")) {
    var sel = $("#main").find(window.location.hash);
    if (sel[0]) { sel[0].scrollIntoView({ behavior: "smooth" }); }
  }
});
