const _dom = {};

$(document)
    .ready(function () {
        getDomEl();
        showHideBlock();
        workWithSwapInput();
        cancelWorker();
        swapWorker();
        rescheduleWorker();
    });

function cancelWorker() {
    _dom["cancelRehearsalAction"] = $("button[rehearsal-id]");
    _dom.cancelRehearsalAction.on("click", (ev) => {
        const _button = ev.currentTarget;
        const rId = _button.getAttribute("rehearsal-id");
        if (rId) {
            const userRow = _button.parentElement.parentElement;
            disableRow(userRow);
            _dom.overlay.show();
            $.ajax(`/cancel/${rId}`, {
                method: "GET"
            }).done((res) => {
                _dom.overlay.hide();
                updatePage(res);
            })
        }
    });
}

function swapWorker() {
    _dom.swapAction.on("click", () => {
        $('#swap').hide();
        const checkedEl = $("input[name='swap']:checked");
        checkedEl.each((i, e) => {
            disableRow(e.parentElement.parentElement);
        });
        const ids = ([]).slice
            .call(checkedEl)
            .map(i => i.value);
        _dom.overlay.show();
        $.ajax("/swap", {
            method: "POST",
            contentType: "text/plain",
            data: `${ids}`
        }).done(res => {
            _dom.overlay.hide();
            updatePage(res);
        })
    })
}

function rescheduleWorker() {
    _dom.generateListAction.on("click", () => {
        const member = $(`select[name="member"]`).get(0);
        const half = $(`input[name="half"]`).get(0);
        const date = $(`input[name="date"]`).get(0);
        const data = {
            date: date.value,
            member: member.value,
            half: half.checked
        };
        _dom.overlay.show();
        disableRehearsals();
        $.ajax("/generate", {
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(data)
        }).done(res => {
            _dom.overlay.hide();
            updatePage(res);
        })
    })
}

function disableRehearsals() {
    ([]).slice
        .call(document.getElementsByClassName("(╯°□°）╯︵ ┻━┻"))
        .forEach(row => {
            disableRow(row);
        });
}

function updatePage(res) {
    parseJson(res)
        .then(rehearsals => {
            regenerateRehearsalsRows(rehearsals);
            setTitle(
                rehearsals[0].date,
                rehearsals[0].weekday,
                rehearsals[0].member
            );
        });
}

function regenerateRehearsalsRows(rehearsals) {
    ([]).slice
        .call(document.getElementsByClassName("(╯°□°）╯︵ ┻━┻"))
        .forEach(row => {
            row.parentElement
                .removeChild(row)
        });
    rehearsals.forEach(rehearsal => {
        const row = _dom.rehearsalRowTemplate[0].content.cloneNode(true);
        const tds = $(row).find("td");
        tds.each((i, td) => {
            if (td.className === "r-date")
                td.innerText = rehearsal.date;
            if (td.className === "r-weekday")
                td.innerText = rehearsal.weekday;
            if (td.className === "r-member")
                td.innerText = rehearsal.member;
        });
        $(row).find("button")[0].setAttribute("rehearsal-id", rehearsal.id);
        $(row).find("input")[0].value = rehearsal.id;
        _dom.rehearsalsTable.append(row);
    });
    workWithSwapInput();
    cancelWorker();
}

function setTitle(date, weekday, member) {
    _dom.titleDateEl[0].innerText = `Next rehearsal at ${date}, ${weekday}`;
    _dom.titleMemberEl[0].innerText = member;
}

function getDomEl() {
    _dom["usefulAction"] = $("#useful-action");
    _dom["rehearsalsAction"] = $("#rehearsals-action");
    _dom["rehearsalsEl"] = $("#rehearsals");
    _dom["rescheduleAction"] = $("#reschedule-action");
    _dom["executeEl"] = $("#execute");
    _dom["executeCloseAction"] = $("#execute-close");
    _dom["cardNumber"] = $("#cardNumber");
    _dom["menuEl"] = $("#menu");
    _dom["menuCloseAction"] = $("#menu-close");
    _dom["rehearsalsCloseAction"] = $("#rehearsals-close");
    _dom["cancelRehearsalAction"] = $("button[rehearsal-id]");
    _dom["titleDateEl"] = $("#title-date");
    _dom["titleMemberEl"] = $("#title-member");
    _dom["swapAction"] = $("#swap");
    _dom["overlay"] = $("#overlay");
    _dom["rehearsalRowTemplate"] = $("#rehearsal-row-template");
    _dom["rehearsalsTable"] = $("#rehearsals-table");
    _dom["generateListAction"] = $("#generate-list-action");
}

function workWithSwapInput() {
    $("input[name='swap']").change(function () {
        const maxAllowed = 2;
        let cnt = $("input[name='swap']:checked").length;
        if (cnt > maxAllowed) {
            $(this).prop("checked", "");
            alert('You can select maximum ' + maxAllowed + ' rehearsals!');
            cnt = $("input[name='swap']:checked").length;
        }
        if (cnt === maxAllowed) {
            $('#swap').show();
        } else {
            $('#swap').hide();
        }
    });
}

function showHideBlock() {
    _dom.rehearsalsAction.on("click", () => _dom.rehearsalsEl.show());
    _dom.rehearsalsCloseAction.on("click", () => _dom.rehearsalsEl.hide());
    _dom.rescheduleAction.on("click", () => _dom.executeEl.show());
    _dom.executeCloseAction.on("click", () => _dom.executeEl.hide());
    _dom.usefulAction.on("click", () => _dom.menuEl.show());
    _dom.menuCloseAction.on("click", () => _dom.menuEl.hide());
    _dom.rehearsalsEl.on("click", ev => {
        if (ev.target === _dom.rehearsalsEl.get(0))
            _dom.rehearsalsEl.hide();
    });
    _dom.executeEl.on("click", (ev) => {
        if (ev.target === _dom.executeEl.get(0))
            _dom.executeEl.hide();
    })
}

function disableRow(row) {
    row.style.background = "rgba(0,0,0,0.3)";
    ([]).slice.call(row.getElementsByTagName("*")).forEach(tag => {
        if (tag.disabled !== void 0) {
            tag.disabled = true;
            tag.style.background = "rgba(0,0,0,0.3)";
        }
    });
}

function parseJson(json) {
    return new Promise((resolve, reject) => {
        try {
            const obj = JSON.parse(json);
            resolve(obj);
        } catch (e) {
            reject(e)
        }
    })
}