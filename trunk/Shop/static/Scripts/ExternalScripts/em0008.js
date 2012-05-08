/**
 * Javascript library for template ExtremeMagento
 * @copyright 2007 Quick Solution LTD. All rights reserved.
 * @author Giao L. Trinh <giao.trinh@quicksolutiongroup.com>
 */

(function() {
	
// EM.tools {{{
	
if (typeof BLANK_IMG == 'undefined') 
	var BLANK_IMG = '';

// declare namespace() method
String.prototype.namespace = function(separator) {
  this.split(separator || '.').inject(window, function(parent, child) {
    var o = parent[child] = { }; return o;
  });
};


'EM.tools'.namespace();

EM.tools.roundedCorner = function (selector) {
	$$(selector).each(function(el) {
		$(el).addClassName('em-rounded');
		$(el).insert({
			top: '<span class="tl"> </span><span class="tm"> </span><span class="tr"> </span><span class="ml"> </span><span class="mm"> </span><span class="mr"> </span><span class="bl"> </span><span class="bm"> </span><span class="br"> </span>'
		});
	});
};
EM.tools.roundedCornerTextBox = function () {
	$$('.input-text').each(function(el) {
		if (Element.visible(el) && !el.hasClassName('qty')) {
			$(el).relativize();
			$(el.parentNode).addClassName('em-rounded');
			$(el.parentNode).insert({
				top: '<span class="tl"> </span><span class="tm"> </span><span class="tr"> </span><span class="ml"> </span><span class="mm"> </span><span class="mr"> </span><span class="bl"> </span><span class="bm"> </span><span class="br"> </span>'
			});
		}
	});
};



// EM0008 {{{
	
function decorateCatalogProductView() {
	if (Element.hasClassName(document.body, 'catalog-product-view')) {
		$$('.short-description h2, .product-collateral h2').each(function(el) {
			el.innerHTML = '<span>'+el.innerHTML+'</span>';
		});
	}
}

function decorateSlideshow() {
	var $$li = $$('.slideshow ul li');
	if ($$li.length > 0) {
		
		// reset UL's width
		var ul = $$('.slideshow ul')[0];
		var w = 0;
		$$li.each(function(li) {
			w += li.getWidth();
		});
		ul.setStyle({'width':w+'px'});
		
		// private variables
		var previous = $$('.slideshow a.previous')[0];
		var next = $$('.slideshow a.next')[0];
		var num = 3;
		var width = ul.down().getWidth() * num;
		var slidePeriod = 3; // seconds
		var manualSliding = false;
		
		// next slide
		function nextSlide() {
			new Effect.Move(ul, { 
				x: -width,
				mode: 'relative',
				queue: 'end',
				duration: 1.0,
				transition: Effect.Transitions.sinoidal,
				afterFinish: function() {
					for (var i = 0; i < num; i++)
						ul.insert({ bottom: ul.down() });
					ul.setStyle('left:0');
				}
			});
		}
		
		// previous slide
		function previousSlide() {
			new Effect.Move(ul, { 
				x: width,
				mode: 'relative',
				queue: 'end',
				duration: 1.0,
				transition: Effect.Transitions.sinoidal,
				beforeSetup: function() {
					for (var i = 0; i < num; i++)
						ul.insert({ top: ul.down('li:last-child') });
					ul.setStyle({'position': 'relative', 'left': -width+'px'});
				}
			});
		}
		
		
		// bind next button's onlick event
		next.observe('click', function(event) {
			Event.stop(event);
			manualSliding = true;
			nextSlide();
		});
		
		// bind previous button's onclick event
		previous.observe('click', function(event) {
			Event.stop(event);
			manualSliding = true;
			previousSlide();
		});
		
		
		// auto run slideshow
		new PeriodicalExecuter(function() {
			if (!manualSliding) nextSlide();
			manualSliding = false;
		}, slidePeriod);
		
		
	}
}

document.observe("dom:loaded", function() {
	decorateCatalogProductView();
	decorateSlideshow();
});

// }}}

})();