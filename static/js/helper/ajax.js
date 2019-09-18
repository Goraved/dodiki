export class Ajax {
    xhr;
    url;
    headers;
    method;

    constructor(url) {
        this.xhr = new XMLHttpRequest();
        this.url = url;
    }

    setHeader(headers) {
        this.headers = headers;
        return this
    }

    get() {
        this.method = "GET";
        this._send();
    }

    post(body) {
        this.method = "POST";
        this._send(body);
    }

    onResponse(cb) {
        this.xhr.onreadystatechange = () => {
            if (this.xhr.readyState === 4)
                cb(this.xhr);
        };
        return this;
    }

    _send(body) {
        this.xhr.open(this.method, this.url);
        if (this.headers)
            for (let [k, v] of Object.entries(this.headers))
                this.xhr.setRequestHeader(k, v);
        this.xhr.send(typeof (body) === "string" ? body : JSON.stringify(body));
    }
}