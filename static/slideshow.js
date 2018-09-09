function addSlideImgs(slideImgsDir, slideFilenames, showCaptions) {
    var container = document.querySelector('.slideshow-container');
    var containerHeight = container.clientHeight.toString() + "px";
    
    // Set line-height to the container div height for vertical img alignment
    container.style.lineHeight = containerHeight;
    
    for (var i = 0; i < slideFilenames.length; i++) {
        var slideFilename = slideFilenames[i];
        var slideFig = document.createElement("figure");
        if (i == 0) {
            slideFig.classList.add("show");
        }
        var slideImg = document.createElement("img");
        slideImg.src = slideImgsDir + slideFilename;
        // Set the max-height dynamicaly, as different slideshow containers may have different heights.
        slideImg.style.maxHeight = containerHeight;
        slideFig.appendChild(slideImg);
        if (showCaptions && slideFilename.indexOf("cap=") == 0) {
            var slideText = slideFilename.substring(4, slideFilename.lastIndexOf('.'));
            var slideCap = document.createElement("figcaption");
            slideCap.innerHTML = slideText;
            slideFig.appendChild(slideCap);
        }
        container.appendChild(slideFig);
    }
    
    // Add control spans
    var prevSpan = document.createElement("span");
    prevSpan.classList.add("prev");
    prevSpan.classList.add("non-selectable");
    prevSpan.innerHTML = "&laquo";
    container.appendChild(prevSpan);
    
    var nextSpan = document.createElement("span");
    nextSpan.classList.add("next");
    nextSpan.classList.add("non-selectable");
    nextSpan.innerHTML = "&raquo";
    container.appendChild(nextSpan);
    
    var pauseSpan = document.createElement("span");
    pauseSpan.classList.add("pause");
    pauseSpan.classList.add("non-selectable");
    pauseSpan.innerHTML = "pause"
    container.appendChild(pauseSpan);
}

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