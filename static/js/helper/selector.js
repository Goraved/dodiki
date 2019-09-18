export function selector(selectBy) {
    let selectedEl = [];
    const _firstChar = selectBy.charAt();
    if (selectBy.charAt() === "#")
        selectedEl = document.getElementById(selectBy);
    else {
        const match = selectBy.match(/^([\#\.\w\d]*)(?:\[(.*)[?=\]]|$)[\:]?(.*)/);
        if (match) {
            const _name = match[1];
            const _attr = match[2] && match[2].split("=");
            const _conditionAttr = match[3];
            if (_name.charAt(0) === ".") {
                selectedEl = ([]).slice.call(document.getElementsByClassName(selectBy));
            } else {
                selectedEl = ([]).slice.call(document.getElementsByTagName(selectBy));
            }
            if (_attr)
                selectedEl.forEach(el => {

                })
        }
    }
    return selectedEl;
}

//"asdf[aaa]:a".match(/^([\#\.\w\d-]*)(?:\[(.*)\])?(?:\:(.*))?/)

// /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/