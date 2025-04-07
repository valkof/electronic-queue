const word = 'привет';

let enWord = encodeURIComponent(word);
console.log(enWord);

enWord = unescape(enWord);
console.log(enWord);

enWord = window.btoa(enWord);
console.log(enWord);