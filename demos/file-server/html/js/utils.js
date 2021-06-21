$.fn.enterKey = function (fnc) {
    return this.each(function () {
        $(this).keypress(function (ev) {
            var keycode = (ev.keyCode ? ev.keyCode : ev.which);
            if (keycode == "13") {
                fnc.call(this, ev);
            }
        })
    })
}

$.fn.escapeKey = function (fnc) {
    return this.each(function () {
        $(this).keypress(function (ev) {
            var keycode = (ev.keyCode ? ev.keyCode : ev.which);
            if (keycode == "27") {
                fnc.call(this, ev);
            }
        })
    })
}

function numCharSets(str) {
  var n = 0;
  if (/[a-z]/.test(str)) { n++; }
  if (/[A-Z]/.test(str)) { n++; }
  if (/[0-9]/.test(str)) { n++; }
  if (/[^a-zA-Z0-9]/.test(str)) { n++; }
  return n;
}

function postLogin() {
  debugLog("Post login")
  $("#login").hide();
  $("#logout").show();
  $.each(postLoginHooks, function (i, f) { f(); });
}

function postLogout() {
  debugLog("Post logout")
  $("#logout").hide();
  $("#login").show();
  $.each(postLogoutHooks, function (i, f) { f(); });
}

function loggedInUser() {
  var access_token = localStorage.getItem("access_token");
  var username = localStorage.getItem("username");
  if (access_token !== null && username !== null) {
    return { username: username, access_token: access_token };
  }
}

function animateProgressBar(barId, total_time, start, callback) {
  function frame() {
    curr++;
    if (curr >= 100) {
      barInner.css("width", "100%");
      clearInterval(advance);
      if (callback) { callback(barId); }
      return;
    }
    barInner.css("width", curr + "%");
  }
  var curr = start || 0;
  var barInner = $("#" + barId + " div.progress-bar-inner");
  if (curr > 100) { curr = 100; }
  barInner.css("width", curr + "%");
  var advance = setInterval(frame, total_time * 1000 / (100 - curr));
  timers["progress-bar-" + barId] = advance;
}

function markProgressBarAsDone(barId) {
  stopProgressBar(barId);
  $("#" + barId + " div.progress-bar-inner")
    .removeClass("error")
    .addClass("done").css("width", "100%");
}

function markProgressBarAsStuck(barId) {
  stopProgressBar(barId);
  $("#" + barId + " div.progress-bar-inner")
    .removeClass("done").addClass("error");
}

function stopProgressBar(barId) {
  var advance = timers["progress-bar-" + barId];
  clearInterval(advance);
}

function resetProgressBar(barId) {
  stopProgressBar(barId);
  var barInner = $("#" + barId + " div.progress-bar-inner");
  barInner.css("width", "0");
  barInner.removeClass("done error");
}

function progressBar(id) {
  var cont = $('<div class="progress-bar">');
  if (id !== undefined && id !== null) { cont.attr("id", id); }
  $('<div class="progress-bar-inner"/>').appendTo(cont);
  return cont;
}

function downloadData(data, filename) {
  var URL = window.URL || window.webkitURL;
  if (is_str(data)) {
    data = new Blob([data], {type: "text/plain"});
  }
  var blob_url = URL.createObjectURL(data);

  var a = $("<a/>");
  a.attr("href", blob_url);
  if (filename) { a.attr("download", filename); }
  a.hide().appendTo("body")
  a[0].click();
  a.remove();
  URL.revokeObjectURL(blob_url);
}

function blobDownloadLink(data, filename, label) {
  if (label === undefined || label === null) {
    label = "Click to download"; }

  var a = $('<a href="#"/>').text(label);
  a.click(function (evt) {
    evt.preventDefault();
    downloadData(data, filename);
  });
  return a;
}

function scrollTo(anchor) {
  var elem = $("#main").find(anchor);
  if (elem) {
    elem[0].scrollIntoView({ behavior: "smooth" });
    history.replaceState(null, "", anchor)
  }
}

function openInNewTab(url) {
  window.open(url, "_blank").focus();
}

function openInSameTab(url) {
  window.location.href = url;
  // window.open(url, "_self");
}

function debugLog(msg) {
  if (debug) { console.log(msg); }
}

function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch (e) {
    return null;
  }
}

function currTimestamp() {
  return Math.floor(+ new Date() / 1000);
}

function jwtHasExpired(token) {
  var parsed = parseJwt(token);
  if (! parsed || ! parsed["exp"]) { return true; }
  return parsed["exp"] <= currTimestamp();
}

function is_str(val) {
  return (typeof val === "string" || val instanceof String);
}

function truncate(input, str_length, num_length) {
  function str_truncate() {
    if (str_length === undefined || str_length === null
        || input.length <= str_length) {
      return input;
    } 
    return input.substring(0, str_length - ending.length) + ending;
  }
  function num_round() {
    var m = Math.pow(10, num_length);
    return Math.round((input + Number.EPSILON) * m) / m;
  }

  var ending = "...";
  if (input === undefined || input === null) {
    return "";
  }
  if (is_str(input)) {
    return str_truncate();
  } else {
    return num_round();
  }
};

function setError(msg) {
  $("#title").text(msg).addClass("error");
  $("#topbar .left *").hide();
  $("#title").show();
}

function unsetError() {
  $("#title").text(page_title).removeClass("error");
  $("#topbar .left *").show();
}

function toggleMenuPopup(evt) {
  if ($("#menu").is(":hidden")) {
    showMenuPopup(evt);
  } else {
    hideMenuPopup(evt);
  }
}

function showMenuPopup(evt) {
  evt.stopPropagation();
  $("#menu").show();
  $("body").on("click", null, hideMenuPopup);
}

function hideMenuPopup() {
  $("body").off("click", null, hideMenuPopup);
  $("#menu").hide();
}

function showSelector(label, items) {
  var promise = new Promise(function(resolve, reject) {
    $.each(items, function(i, name) {
      $("<a/>").text(name)
        .appendTo("#selector-popup div.dropdown-content")
        .click(function () {
          resolve($(this).text());
          hideUserSelector();
        });
    });
    $("#selector-popup button.cancel").on("click", null, function () {
      hideUserSelector();
      reject();
    });
  });
  $("#selector-popup button.dropbtn span").text(label);
  $("#selector-popup").show();
  return promise;
}

function hideUserSelector() {
  $("#selector-popup button.cancel").off("click");
  $("#selector-popup div.dropdown-content").empty();
  $("#selector-popup div.dropdown-content").hide();
  $("#selector-popup button.dropbtn span").text();
  $("#selector-popup").hide();
}

function showInputPopup(title, fields, flatten, use_placeholders) {
  var promise = new Promise(function(resolve, reject) {
    $("<h2/>").text(title)
      .insertBefore("#input-popup button[type=submit]");
    $.each(fields, function(alias, default_value) {
      console.log(default_value);
      var input = $('<input type="text"/>')
        .attr("name", alias)
        .attr("value", default_value)
        .prop("required", true)
        .insertBefore("#input-popup button[type=submit]");
      if (use_placeholders) { input.attr("placeholder", alias); }
    });
    $("#input-popup form").submit(function (evt) {
      evt.preventDefault();
      var data = $(this).serializeArray();
      if (flatten) {
        let flat_data = {};
        $.each(data, function (i, dict) {
          flat_data[dict["name"]] = dict["value"]
        });
        resolve(flat_data);
      } else {
        resolve(data);
      }
      hideInputPopup();
    });
    $("#input-popup button.cancel").on("click", null, function () {
      hideInputPopup();
      reject();
    });
  });
  $("#input-popup").show();
  $("#input-popup input:first").focus();
  return promise;
}

function hideInputPopup() {
  $("#input-popup button.cancel").off("click");
  $("#input-popup form").off("submit");
  $("#input-popup h2, #input-popup input").remove();
  $("#input-popup").hide();
}

function showErrorPopup(err, timeout) {
  if (err) { showAlertPopup(err, false, timeout); }
}

function showAlertPopup(message, ok, timeout) {
  if (timeout === undefined || timeout === null) {
    timeout = 2500;
  }
  debugLog(message);
  $("#alert-popup h2").text(message);
  $("#alert-popup").addClass("fade-in");
  $("#alert-popup").removeClass("fade-out");
  if (! ok) {
    $("#alert-popup").addClass("bad");
  }
  $("#alert-popup").on("click", null, hideAlertPopup);
  $("#alert-popup").show();
  if (timeout > 0) {
    setTimeout(hideAlertPopup, timeout);
  }
}

function hideAlertPopup() {
  $("#alert-popup h2").text();
  $("#alert-popup").addClass("fade-out");
  $("#alert-popup").removeClass("fade-in");
  $("#alert-popup").off("click", null, hideAlertPopup);
  setTimeout(function () {
    $("#alert-popup").hide();
    $("#alert-popup").removeClass("bad");
  }, 1000);
}

function showLoginPopup(evt) {
  function action(evt, resolve, reject) {
    debugLog("Logging in");
    login(evt)
      .then(function (result) {
        resolve(result);
      })
      .catch(function (err) {
        reject(err);
      });
  }

  var promise = new Promise(function (resolve, reject) {
    $("#login-popup form").on(
      "submit", null, function (evt) {
        $("#login-popup form").off("submit");
        action(evt, resolve, reject);
      });
  });
  $("#login-popup").show();
  $("#login-popup input[name=username]").focus();
  return promise;
}

function hideLoginPopup() {
  $("#login-popup").hide();
  $("#login-msg").text("Login");
  $("#login-popup input[name=username]").val("");
  $("#login-popup input[name=password]").val("");
}

function getMeJSON(method, url, options) {
  return getMe(method, url, options)
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data["error"]) { throw new Error(data["error"]); }
      return data;
    });
}

function getMe(method, url, options, _no_refresh) {
  if (options === undefined) { options = {}; }
  var auth = options["auth"];
  if (auth === undefined) { auth = true; }
  var auth_err_msg = options["auth_err_msg"] || "You are not authorized";
  var headers = options["headers"] || {};
  var body = options["body"];

  if (auth) {
    debugLog(url + " is authenticated");
    var access_token = localStorage.getItem("access_token");
    if (access_token === null || jwtHasExpired(access_token)) {
      if (_no_refresh) {
         // this shouldn't happen
        debugLog("WTF");
        return Promise.reject("Failed to refresh session");
      }
      debugLog("Refreshing session");
      return refreshSession()
        .then(function () {
          return getMe(method, url, options, true);
        });
    }
    headers["Authorization"] = "Bearer " + access_token;
  }

  headers["Content-Type"] =  "application/json; charset=utf-8"
  debugLog("Sending request for " + url);

  var init = {
    method: method,
    headers: headers,
  };
  if (body) { init["body"] = JSON.stringify(body) }

  return fetch(api_prefix + url, init)
    .then(function (response) {
      if (response.status == 401) {
        debugLog("Error: " + auth_err_msg);
        $("#login-msg").text(auth_err_msg);
        unsetError();
        if (auth) {
          debugLog("Resending " + url);
          return showLoginPopup().then(function () {
            return getMe(method, url, options, true);
          });
        } else {
          return showLoginPopup();
        }
      } else if (response.status >= 500) {
        throw new Error(response.statusText);
      }

      return response;
    })
    .catch(function (err) {
      debugLog("Error: " + err.message);
      setError("Cannot connect to the server");
      throw err;
    });
}

function refreshSession() {
  var refresh_token = localStorage.getItem("refresh_token");
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  debugLog("Got refresh token " + refresh_token);
  if (!refresh_token) {
    debugLog("No refresh token");
    return showLoginPopup();
  }
  return getMeJSON("POST", "/authtoken",
      {
        body: { refresh_token: refresh_token },
        auth: false, auth_err_msg: "Session expired",
      })
    .then(function (data) {
      if (data["refresh_token"]) {
        debugLog("Updating refresh token");
        localStorage.setItem("refresh_token", data["refresh_token"]);
      }
      localStorage.setItem("access_token", data["access_token"]);
      return Promise.resolve(data);
    });
}

function login(evt) {
  if (evt) { evt.preventDefault(); }
  return getMeJSON("POST", "/login",
      {
        body: {
          username: $("#login-popup input[name=username]").val(),
          password: $("#login-popup input[name=password]").val()
        },
        auth: false, auth_err_msg: "Wrong username or password",
      })
    .then(function (data) {
      debugLog("Saving new access and refresh tokens");
      localStorage.setItem("refresh_token", data["refresh_token"]);
      localStorage.setItem("access_token", data["access_token"]);
      localStorage.setItem("username",
        $("#login-popup input[name=username]").val());
      postLogin();
      hideLoginPopup();
      return Promise.resolve(data);
    });
}

function logout(evt) {
  if (evt) { evt.preventDefault(); }
  return getMe("POST", "/logout",
      {
        body: { refresh_token: localStorage.getItem("refresh_token") },
        auth: false,
      })
    .then(function () {
      scores = localStorage.getItem("latest_scores");
      localStorage.clear();
      localStorage.setItem("latest_scores", scores);
      postLogout();
    });
}

function addPopup(id, title) {
  var popup = $('<div class="popup" id="' + id + '"/>')
    .appendTo("body");
  var container = $('<div class="popup-container"/>').appendTo(popup);
  if (title !== undefined && title !== null) {
    $("<h2/>").text(title).appendTo(container);
  }
  return container;
}

function addScrollPopup(id, title, action_label, cancel_label) {
  var popup = addPopup(id, title);
  var content = $('<div class="scroll" />').appendTo(popup);
  if (action_label) {
    var action = addButton(action_label, null, "action")
      .appendTo(popup);
  }
  if (cancel_label) {
    var cancel = addButton(cancel_label, null, "cancel").appendTo(form);
    if (action_label) {
      action.addClass("narrow left");
      cancel.addClass("narrow right");
    }
  }
  if (! action_label && ! cancel_label) {
    popup.addClass("full-body");
  }
  return popup;
}

function addPopupGrid(container, rows, no_header, rotate) {
  var table = $("<table/>").appendTo(container);
  if (rotate) {
    table.addClass("rotate");
  }
  var tbody = $("<tbody/>").appendTo(table);
  var thead;
  if (no_header) { thead = tbody; }
  else { thead = $("<thead/>").prependTo(table); }
  $.each(rows, function(i, cells) {
    var target = tbody;
    if (i == 0) { target = thead; }
    var row = $("<tr/>").appendTo(target);
    $.each(cells, function(j, val) {
      var cell = "td";
      if (i == 0 && ! no_header) { cell = "th"; }
      var cell_el = $("<" + cell + "/>").appendTo(row);
      if (is_str(val)) {
        cell_el.text(val);
      } else {
        cell_el.html(val);
      }
    });
  });
  return table;
}

function addPopupForm(container, title, inputs,
                      submit_label, cancel_label) {
  var form = $('<form action="#" class="popup-container"/>')
    .appendTo(container);
  if (title !== undefined && title !== null) {
    var heading = $("<h2/>").appendTo(form);
    var heading_text;
    if (is_str(title)) {
      heading_text = title;
    } else {
      heading_text = title["text"] || "";
      if (title["id"]) {
        heading.attr("id", title["id"]);
      }
    }
    heading.text(heading_text);
  }
  $.each(inputs, function(name, obj) {
    var input = $('<input name="' + name + '"/>').appendTo(form);
    $.each(obj["attrs"], function(key, val) {
      input.attr(key, val);
    });
    $.each(obj["props"], function(key, val) {
      input.prop(key, val);
    });
  });
  var submit = addButton(submit_label, null, "action", "submit")
    .appendTo(form);
  if (cancel_label) {
    addButton(cancel_label, null, "cancel").appendTo(form)
      .addClass("narrow right");
    submit.addClass("narrow left");
  }
  return form;
}

function addImagePopup(id, images) {
  var popup = addScrollPopup(id).addClass("wide");
  var content = popup.find("div:first");
  $.each(images, function (i, src) {
    $('<img src="' + src + '" alt=""/>').appendTo(content);
  });
  addButton("", null, "cancel").appendTo(popup)
    .click(function () { $("#" + id).hide(); });
  $("#" + id).click(function (evt) {
    if (this !== evt.target) { return; }
    $(this).hide();
  });
  return content;
}

function addMenuItem(id, label, action) {
  return $('<p id="' + id + '"/>').text(label)
    .insertBefore("#menu button:first")
    .click(action);
}

function addMenuSep() {
  return $('<div class="sep" />')
    .insertBefore("#menu button:first");
}

function addTopbarItem(item, align) {
  var cont = $('<span class="' + align + '"/>').appendTo("#topbar");
  return $(item).appendTo(cont);
}

function addValidityCheck(input, checker, msg) {
  input.on("invalid", null, function (evt) { evt.preventDefault(); });
  input.on("input", null, function onInput(evt) {
    if ($(this).val() && ! checker.bind(this)()) { bubble.show(); }
    else { bubble.hide(); }
  });
  var bubble = $("<div/>").addClass("validity-msg").hide()
    .insertAfter(input)
  $("<p/>").text(msg).appendTo(bubble);
  return bubble;
}

function addButton(label, id, cls, type) {
  var button = $("<button/>");
  if (id !== undefined && id !== null) {
    button.attr("id", id);
  }
  if (cls !== undefined && cls !== null) {
    button.addClass(cls);
  }
  if (type !== undefined && type !== null) {
    button.attr("type", type);
  }
  $("<span/>").text(label).appendTo(button);
  return button;
}
