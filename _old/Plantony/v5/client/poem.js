// function to load the poem from the JSON file
function loadPoem(callback) {
  $.getJSON("poem.json", function(data) {
    callback(data);
  });
}

// function to display the poem using a fade effect
function displayPoem(poem) {
  // create a new HTML element to hold the poem
  var $poemElement = $("<div>");

  // add the prompt and epoch to the element
  $("<h1>").text(poem.weaving).appendTo($poemElement);
  $("<h2>").text(poem.epoch).appendTo($poemElement);

  // add each line of the poem to the element with a fade effect
  $.each(poem.lines, function(index, line) {
    $("<p>")
      .text(line)
      .hide()
      .appendTo($poemElement)
      .fadeIn(index * 500);
  });

  // get the Epoch time value from the JSON object
  const epochTime = poem.lines[3].EpochTime;

  // convert the Epoch time value to a human-readable format
  const date = new Date(epochTime * 1000);
  const dateString = date.toLocaleString();

  // add the elapsed time since Epoch to the element
  $("<p>").text(`Elapsed time since Epoch: ${dateString}`).appendTo($poemElement);

  // remove the previous poem element, if any
  $("#poem-container").remove();

  // add the poem element to the body of the HTML document
  $("body").append($("<div>").attr("id", "poem-container").append($poemElement));
}

// load the poem and display it
loadPoem(displayPoem);
