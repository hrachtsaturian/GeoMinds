function selectChoice(id, isAnswered) {
  if (isAnswered === "True") {
    return;
  }
  $("#selectedChoice").val(id);
  $("#confirmButton").prop("disabled", false);
  $("[id^='choice-']").attr("class", "btn btn-outline-primary");
  $(`#choice-${id}`).attr("class", "btn btn-warning");
}

function redirectToPage(next) {
  window.location.href = next;
}

async function runTimer(createdAtUTC, currentTimeUTC) {
  const difference = currentTimeUTC - createdAtUTC;
  const differenceSec = 300 - Math.round(difference / 1000);
  let minutes = Math.floor(differenceSec / 60);
  let seconds = differenceSec - minutes * 60;

  if (minutes < 0) {
    minutes = 0;
    seconds = 0;
  }

  $(document).ready(function () {
    $(".timer").html(
      `<p>Time remaining ${minutes}:${
        seconds < 10 ? `0${seconds}` : seconds
      }</p>`
    );
    if (minutes < 1) {
      $(".timer").css("color", "red");
    }
  });
  if (differenceSec <= 0) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    window.location.reload();
  }
}

async function startTimer(createdAt, currentTime) {
  const createdAtUTC = new Date(createdAt);
  const currentTimeUTC = new Date(currentTime);
  let countDown = 0
  await runTimer(createdAtUTC, currentTimeUTC);
  setInterval(() => {
    countDown += 1000
    runTimer(createdAtUTC, new Date(currentTimeUTC.getTime() + countDown));

  }, 1000);
}

$(document).ready(() => {
  $("form").on("submit", () => {
    $("#confirmButton").prop("disabled", true);
    $("#startGame").prop("disabled", true);
    $("#confirmEditButton").prop("disabled", true);
    $("#deleteUserButton").prop("disabled", true);
  });
});
