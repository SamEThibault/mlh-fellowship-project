// this script takes care of the typewriter animation on the home page "/"

const TypeWriter = function(txtElement, words, wait = 1500) {
    this.txtElement = txtElement;
    this.words = words
    this.txt = '';
    this.wordIndex = 0;
    this.wait = parseInt(wait, 10)
    this.type();
    this.isDeleting = false;
    this.done = false
}

// Type Method
TypeWriter.prototype.type = function () {
    const currentIndex = this.wordIndex;
    const fullTxt = this.words[currentIndex];

    if (this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
    }

    this.txtElement.innerHTML = `<span class="txt">${this.txt}</span>`;

    let typeSpeed = 50;

    if (this.isDeleting) typeSpeed /= 2;

    if (!this.isDeleting && this.txt === fullTxt && this.wordIndex + 1 === this.words.length) {
        this.done = true;
    } else if (!this.isDeleting && this.txt === fullTxt) {
        typeSpeed = this.wait;
        this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
        typeSpeed = 500;
        this.isDeleting = false;
        this.wordIndex++;
    }

    if (this.done) {
        setTimeout(() => {
            this.txtElement.classList.toggle('blink');
        }, 1800);
        return;
    }
    else {
        setTimeout(() => this.type(), typeSpeed)
    }
}

function delay(time) {
  return new Promise(resolve => setTimeout(resolve, time));
}

//Init App
function init() {
    const txtElement = document.querySelector('.txt-type');
    const words = JSON.parse(txtElement.getAttribute('data-words'));
    const wait = txtElement.getAttribute('data-wait');

    new TypeWriter(txtElement, words, wait);
}

setTimeout(init, 1000)