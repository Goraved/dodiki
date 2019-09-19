export function parseJson(json) {
    return new Promise((resolve, reject) => {
        try {
            const obj = JSON.parse(json);
            resolve(obj);
        } catch (e) {
            reject(e)
        }
    })
}