_import("./helper/copy-card.js", "copyCardNumber");

function _import(path, name) {
    import(path)
        .then((module) => {
            window["dUtils"] = window["dUtils"] || {};
            window["dUtils"][name] = module[name];
        })
        .catch(err => {
            console.log(`%cERROR IMPORT: path - ${path}, name - ${name}, err - ${err}`, "color:red");
        })
}

function copyToClipboard(element) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
}
