$(document).ready(function() {
    $('.pgwSlideshow').pgwSlideshow();
    setFirstImageMargin();
});

$(window).load(function() { 
	setImageTopMargins();
});

function showLightbox() {
    // .slice(0) is neccessary beacuse hiddenImages is mutable
    var tempImages = hiddenImages.slice(0);

    var shiftedImages = tempImages.concat(tempImages.splice(0, slideIndex));

    $.SimpleLightbox.open({
        items: shiftedImages
    });
}

function setImageTopMargins() {
	// center main image in slideshow, kind of a hacky way of correcting image height but since we have no way of knowing
  // the image dimensions provided by the backend, this function adds a margin to the top of every image after it loads
  // based on the height of the images. display:flex applied to images corrects their positioning in the slideshow, but
  // doing so breaks slide transitions.

  var marginLoopIndex = 0;
	$('.main-slide-image').each(function(i, obj) {
    if (marginLoopIndex != 0) {
   		var height = $(this).height();
   		if (400 - height > 1) {
        $(this).css({'margin-top': ((400 - height) / 2) + 'px'});
      }
    }
    marginLoopIndex += 1;
  });
}

// This calculates and sets the first image margin so there isn't a visible delay in margins being applied to images.
// document.ready can be messy when dealing with partial postbacks and also runs before all the images are loaded
// window.load runs after everything in the page has loaded, but by doing so there is a noticeable delay on the first
// visible image. So instead, we check for the first image to be loaded asynchronously every 50ms until it loads.

var firstImageHeight = 0;
function setFirstImageMargin () {
   setTimeout(function () {
      firstImageHeight = $('.elt_1').height();
      if (firstImageHeight === 0) {
        setFirstImageMargin();
      } else {
        if (400 - height > 1) {
          $('.elt_1.main-slide-image').css({'margin-top': ((400 - firstImageHeight) / 2) + 'px'});
        }
      }
   }, 50)
}
