import TypeIt from 'typeit'

// Override of Toha's scripts/pages/home.js: faster typing, and a pause holding
// the fully-typed string on screen before it deletes (upstream has neither).
document.addEventListener('DOMContentLoaded', () => {
  const $ul = document.getElementById('typing-carousel-data')?.children
  if ($ul == null || $ul.length === 0) return

  const strings = Array.from($ul).map($el => $el.textContent)

  let typeItInstance = new TypeIt('#typed', {
    speed: 40,
    deleteSpeed: 20,
    lifeLike: false,
    breakLines: false,
    cursorChar: "|",
    waitUntilVisible: true,
    html: false,
    loop: true
  })

  strings.forEach((string, index) => {
    typeItInstance = typeItInstance.type(string).pause(2000)
    if (index < strings.length - 1) {
      typeItInstance = typeItInstance.delete(string.length)
    }
  })

  typeItInstance.go()
})
