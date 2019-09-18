export function copyCardNumber() {
    /* Get the text field */
    const copyText = document.getElementById("cardNumber");

    /* Select the text field */
    copyText.select();

    /* Copy the text inside the text field */
    document.execCommand("copy");

    /* Alert the copied text */
    alert("Copied the text: " + copyText.value);
}