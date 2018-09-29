function setupSlideEvents() {
    var counter = 0;
    var $items = document.querySelectorAll('.slideshow-container figure');
    var numItems = $items.length;

    var showCurrent = function() {
      var itemToShow = Math.abs(counter % numItems);
      [].forEach.call( $items, function(el){
        el.classList.remove('show');
      });
      $items[itemToShow].classList.add('show');
    };

    var paused = false;
    function nextSlide() {
        if (!paused){
            counter++;
            showCurrent();
        }
    }
    var slideInterval = setInterval(nextSlide, 3000);

    document.querySelector('.next').addEventListener('click', function() {
        counter++;
        showCurrent();
    }, false);
    document.querySelector('.prev').addEventListener('click', function() {
        counter--;
        showCurrent();
    }, false);

    var pauseButton = document.querySelector('.pause');
    pauseButton.addEventListener('click', function() {
        if (paused){
            pauseButton.innerHTML = "pause";
            paused = false;
        }else{
            pauseButton.innerHTML = "play";
            paused = true;
        }
    }, false);
}