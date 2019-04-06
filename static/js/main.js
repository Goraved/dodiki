function copyCardNumber() {
  /* Get the text field */
  var copyText = document.getElementById("cardNumber");

  /* Select the text field */
  copyText.select();

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);
}

$(document).ready(function () {
    $("input[name='swap']").change(function () {
        var maxAllowed = 2;
        var cnt = $("input[name='swap']:checked").length;
        if (cnt > maxAllowed) {
            $(this).prop("checked", "");
            alert('You can select maximum ' + maxAllowed + ' rehearsals!');
            cnt = $("input[name='swap']:checked").length;
        }
        if (cnt === maxAllowed) {
            $('#swap').show();
        }
        else {
            $('#swap').hide();
        }

    });
});