(function($){

  function PolarClock(el, options){
    this.el = $(el)
    this.radius = options.radius || 100;
    this.inner_radius = options.inner_radius || 80;
    this.curr_z = options.start_z || 0;
    this.color = options.color || '#F00';
    this.bg_color = options.bg_color || '#FFF';
    this.rotators = [];
    this.startcorners = [];
    this.degrees = options.degrees || 180;
    this.duration = (options.rate?options.rate*this.degrees:null) ||options.duration || 1000;
  
    this.initialize();
    if(options.immediate)
      this.animate();
  }
  
  $.fn.polarClock = function(options) {
    return new PolarClock(this.get(0), options);
  };
  
  function makeSemiCircle(options){
    var cornerElems = {topleft:['borderTopLeftRadius','-moz-border-radius-topleft','-webkit-border-radius-topleft'],
                       topright:['borderTopRightRadius','-moz-border-radius-topright','-webkit-border-radius-topright'],
                       bottomright:['borderBottomRightRadius','-moz-border-radius-bottomright','-webkit-border-radius-bottomright'],
                       bottomleft:['borderBottomLeftRadius','-moz-border-radius-bottomleft','-webkit-border-radius-bottomleft']};
    var me = options.me;
    var css = {'background-color':options.color,'z-index':me.curr_z++,'width':options.side,'height':options.side, 'position':'absolute',left:options.left,top:options.top};
    for(var i=0;i<(cornerElems[options.corner]).length;i++)
      css[cornerElems[options.corner][0]] = options.side; 
    css[options.corner] = options.side;
    if(options.to) $.extend(css, {'transform-origin:':options.to,'-webkit-transform-origin':options.to,'-moz-transform-origin':options.to,'-o-transform-origin':options.to});
    return $('<div></div>').css(css).appendTo(options.inner);
  }
  
  PolarClock.prototype = {
    initialize:function(){
      var self = this;
      self.el.css({'height':self.radius * 2,'width':self.radius * 2,'z-index':self.curr_z++,'background-color':'transparent'});
      var inner = $('<div></div>').css({'position':'relative'}).appendTo(self.el);
      
      self.startcorners[0] = makeSemiCircle({me:self, inner:inner, corner:'topright', side:self.radius, top:0, left:self.radius, color:self.color});
      self.startcorners[1] = makeSemiCircle({me:self, inner:inner, corner:'topright', side:self.inner_radius, top:(self.radius-self.inner_radius), left:self.radius, color:self.bg_color});
      self.rotators[0] = makeSemiCircle({me:self, inner:inner, corner:'topright', side:self.radius + 1, top:-1, left:self.radius, color:self.bg_color, to:'0% 100%'});
      
      if(self.degrees > 90){
        makeSemiCircle({me:self, inner:inner, corner:'bottomright', side:self.radius, top:self.radius, left:self.radius, color:self.color});
        makeSemiCircle({me:self, inner:inner, corner:'bottomright', side:self.inner_radius, top:self.radius, left:self.radius, color:self.bg_color});
      }
      self.rotators[1] = makeSemiCircle({me:self, inner:inner, corner:'bottomright', side:self.radius + 1, top:self.radius, left:self.radius, color:self.bg_color, to:'0% 0%'});
      if(self.degrees > 180){
        makeSemiCircle({me:self, inner:inner, corner:'bottomleft', side:self.radius, top:self.radius, left:0, color:self.color});
        makeSemiCircle({me:self, inner:inner, corner:'bottomleft', side:self.inner_radius, top:self.radius, left:(self.radius - self.inner_radius), color:self.bg_color});
      }
      self.rotators[2] = makeSemiCircle({me:self, inner:inner, corner:'bottomleft', side:self.radius + 1, top:self.radius, left:-1, color:self.bg_color, to:'100% 0%'});
      if(self.degrees > 270){
        makeSemiCircle({me:self, inner:inner, corner:'topleft', side:self.radius, top:0, left:0, color:self.color});
        makeSemiCircle({me:self, inner:inner, corner:'topleft', side:self.inner_radius, top:(self.radius - self.inner_radius), left:(self.radius - self.inner_radius), color:self.bg_color})
      }
      self.rotators[3] = makeSemiCircle({me:self, inner:inner, corner:'topleft', side:self.radius + 1, top:-1, left:-1, color:self.bg_color, to:'100% 100%'});
    },
    animate:function(){
      var self = this;
      var degrees_step = self.duration/self.degrees;
      var degrees_left = self.degrees;
      var rotator = 0;
      function startAnimation(){
        if(degrees_left > 0){
          if(rotator == 3){
            self.startcorners[0].css('z-index',self.curr_z++);
            self.startcorners[1].css('z-index',self.curr_z++);
          }
          self.rotators[rotator].css('text-indent', 0).animate({'text-indent': Math.min(degrees_left, 90) }, { step: function(now,fx) { $(this).css({'transform':'rotate('+now+'deg)','-webkit-transform':'rotate('+now+'deg)','-ms-transform':'rotate('+now+'deg)','-moz-transform':'rotate('+now+'deg)','-o-transform':'rotate('+now+'deg)'}); }, duration:(degrees_step*Math.min(degrees_left, 90)), complete:startAnimation, easing:'linear'});
          degrees_left -= 90;
          rotator++;
        }
      }
      startAnimation();
    }
  };

}(jQuery));
