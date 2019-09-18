_import("./helper/ajax.js", "Ajax");
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