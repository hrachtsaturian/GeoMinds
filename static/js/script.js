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

async function runTimer(createdAtUTC) {
  const currentTime = new Date();
  const difference = currentTime - createdAtUTC + 7 * 60 * 60 * 1000;
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

async function startTimer(createdAt) {
  const createdAtUTC = new Date(createdAt);
  await runTimer(createdAtUTC);
  setInterval(() => {
    runTimer(createdAtUTC);
  }, 1000);
}
