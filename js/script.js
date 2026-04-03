document.addEventListener('DOMContentLoaded', function() {
  const slides    = document.querySelectorAll('.slide');
  const iconPause = document.getElementById('iconPause');
  const iconPlay  = document.getElementById('iconPlay');
  const TOTAL     = slides.length;
  const INTERVAL  = 2800;
  const EXIT_MS   = 450;
  let current = 0;
  let locked  = false;
  let playing = true;
  let timer   = null;

  function goTo(next) {
    if (locked || next === current) return;
    locked = true;
    slides[current].classList.add('exit');
    const prev = current;
    setTimeout(() => {
      slides[current].classList.remove('active', 'exit');
      slides[prev].classList.remove('active', 'exit');
      current = next;
      slides[current].classList.add('active');
      locked = false;
    }, EXIT_MS);
  }

  function startTimer() {
    clearInterval(timer);
    timer = setInterval(() => goTo((current + 1) % TOTAL), INTERVAL);
  }

  window.togglePlay = function() {
    playing = !playing;
    if (playing) {
      iconPause.style.display = '';
      iconPlay.style.display  = 'none';
      startTimer();
    } else {
      iconPause.style.display = 'none';
      iconPlay.style.display  = '';
      clearInterval(timer);
    }
  };

  startTimer();
});
